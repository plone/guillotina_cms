from aiohttp.web import StreamResponse
from guillotina import app_settings
from guillotina import configure
from guillotina.api.files import DownloadFile
from guillotina.api.files import _traversed_file_doc
from guillotina.api.service import TraversableFieldService
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IFileManager
from guillotina.response import HTTPNotFound
from guillotina_cms.behaviors.image import IHasImage
from guillotina_cms.interfaces import IImagingSettings
from plone.scale.scale import scaleImage


@configure.service(
    context=IHasImage, method='GET', permission='guillotina.ViewContent',
    name='@@images/{field_name}',
    **_traversed_file_doc('Download the image'))
class DownloadImageFile(DownloadFile):
    pass


@configure.service(
    context=IHasImage, method='GET', permission='guillotina.ViewContent',
    name='@@images/{field_name}/{scale}',
    **_traversed_file_doc('Download the image scale'))
class DownloadImageScale(TraversableFieldService):

    async def __call__(self):
        settings = self.request.container_settings.for_interface(IImagingSettings)
        scale_name = self.request.matchdict['scale']
        allowed_sizes = settings['allowed_sizes']
        if scale_name not in allowed_sizes:
            raise HTTPNotFound(content={
                'reason': f'{scale_name} is not supported'
            })
        file = self.field.get(self.field.context or self.context)
        if file is None:
            raise HTTPNotFound(content={
                'message': 'File or custom filename required to download'
            })

        adapter = get_multi_adapter(
            (self.context, self.request, self.field), IFileManager)
        data = b''
        async for chunk in adapter.iter_data():
            data += chunk

        width, _, height = allowed_sizes[scale_name].partition(':')

        result, format_, size = scaleImage(
            data, int(width), int(height), quality=settings['quality'])

        cors_renderer = app_settings['cors_renderer'](self.request)
        headers = await cors_renderer.get_headers()
        headers.update({
            'CONTENT-DISPOSITION': 'attachment; filename="{}"'.format(
                file.filename)
        })

        download_resp = StreamResponse(headers=headers)
        download_resp.content_type = f'image/{format_}'
        if file.size:
            download_resp.content_length = len(result)

        await download_resp.prepare(self.request)
        await download_resp.write(result)
        await download_resp.drain()
        await download_resp.write_eof()
        return download_resp
