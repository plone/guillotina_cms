from guillotina_cms.fields.interfaces import ICloudImageFileField
from guillotina_cms.fields.interfaces import IImageFile
from guillotina.schema import Object
from zope.interface import implementer


@implementer(ICloudImageFileField)
class CloudImageFileField(Object):
    """
    A cloud file hosted file.

    Its configured on config.json with :

    "cloud_storage": "guillotina.interfaces.IS3FileField"

    or

    "cloud_storage": "guillotina_gcloudstorage.interfaces.IGCloudFileField"

    """

    schema = IImageFile

    def __init__(self, **kw):
        super().__init__(schema=self.schema, **kw)
