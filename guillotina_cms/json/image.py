from guillotina import configure
from guillotina_cms.fields.interfaces import IImageFile
from guillotina_cms.fields.interfaces import ICloudImageFileField
from guillotina_cms.interfaces import IImagingSettings
from guillotina.utils import to_str
from guillotina.utils import get_current_request
from guillotina.files.field import deserialize_cloud_field
from zope.interface import alsoProvides


@configure.value_serializer(for_=IImageFile)
def json_converter(value):
    if value is None:
        return value

    request = get_current_request()
    settings = request.container_settings.for_interface(IImagingSettings)
    scales = {}
    url = request.url.human_repr().split('?')[0]
    for size, dimension in settings['allowed_sizes'].items():
        width, _, height = dimension.partition(':')
        scales[size] = {
            "download": url + '/@@images/image/' + size,
            "height": height,
            "width": width
        }

    return {
        'filename': value.filename,
        'content_type': to_str(value.content_type),
        'size': value.size,
        'extension': value.extension,
        'md5': value.md5,
        'scales': scales
    }


@configure.value_deserializer(ICloudImageFileField)
async def deserialize_image_cloud_field(field, value, context):
    val = await deserialize_cloud_field(field, value, context)
    if val is not None:
        alsoProvides(val, IImageFile)
    return val
