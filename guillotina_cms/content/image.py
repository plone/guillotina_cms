# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Item
from guillotina_cms.interfaces import IImage


@configure.contenttype(
    type_name='Image',
    schema=IImage,
    behaviors=[
        'guillotina.behaviors.dublincore.IDublinCore',
        'guillotina_cms.interfaces.base.ICMSBehavior'],
    allowed_types=[]  # dynamically calculated
)
class Image(Item):
    pass
