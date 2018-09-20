from guillotina import configure
from guillotina import schema
from guillotina.fields import CloudFileField
from guillotina.interfaces import IResource
from zope.interface import Interface


class IHasImage(Interface):
    pass


@configure.behavior(
    title="Image attachment", for_=IResource, marker=IHasImage)
class IImageAttachment(Interface):

    image = CloudFileField()

    caption = schema.TextLine()
