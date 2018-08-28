# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Item
from guillotina_cms.interfaces import IFile


@configure.contenttype(
    type_name='File',
    schema=IFile,
    behaviors=[
        'guillotina.behaviors.dublincore.IDublinCore',
        'guillotina_cms.interfaces.base.ICMSBehavior'],
    allowed_types=[]  # dynamically calculated
)
class File(Item):
    pass
