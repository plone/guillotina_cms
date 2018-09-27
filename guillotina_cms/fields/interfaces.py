from zope.interface import Interface
from guillotina.schema.interfaces import IObject
from guillotina import schema
from guillotina.interfaces import IFile
from guillotina.interfaces import ICloudFileField


class IRichTextField(IObject):
    """Rich text field"""


class IRichTextFieldSchema(Interface):
    """Rich text field schema"""
    content_type = schema.ASCII(
        title='Content type'
    )
    data = schema.Text(
        title='Real data'
    )
    encoding = schema.ASCII(
        title='Get the real encoding'
    )


class IImageFile(IFile):
    """Image file"""

class ICloudImageFileField(ICloudFileField):
    """Image on the cloud file"""