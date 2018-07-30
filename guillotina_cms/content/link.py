# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Item
from guillotina.interfaces import IItem
from guillotina import schema
from guillotina_cms import _
from guillotina.directives import index


class ILink(IItem):

    index('url', type='text')
    url = schema.TextLine(
        title=_('URL'),
        required=False)


@configure.contenttype(
    type_name='Link',
    schema=ILink,
    behaviors=['guillotina.behaviors.dublincore.IDublinCore'],
    allowed_types=[]  # dynamically calculated
)
class Link(Item):
    pass
