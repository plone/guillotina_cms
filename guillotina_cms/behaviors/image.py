from guillotina import configure
from guillotina import schema
from guillotina.fields import CloudFileField
from guillotina.interfaces import IResource
from guillotina_cms.interfaces import IHasImage
from zope.interface import Interface


@configure.behavior(
    title="Image attachment", for_=IResource, marker=IHasImage)
class IImageAttachment(Interface):

    image = CloudFileField()

    caption = schema.TextLine()
