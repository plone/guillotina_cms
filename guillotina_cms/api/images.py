from guillotina import configure
from guillotina.interfaces import IResource
from guillotina.api.files import _traversed_file_doc
from guillotina.api.service import TraversableFieldService
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IFileManager


@configure.service(
    context=IResource, method='GET', permission='guillotina.ViewContent',
    name='@@images/{field_name}',
    **_traversed_file_doc('Download the image of a file'))
class DownloadImageFile(TraversableFieldService):

    async def __call__(self):
        # We need to get the upload as async IO and look for an adapter
        # for the field to save there by chunks
        adapter = get_multi_adapter(
            (self.context, self.request, self.field), IFileManager)
        return await adapter.download()