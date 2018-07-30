# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Item
from guillotina.interfaces import IItem
from guillotina import schema
from guillotina_cms import _
from guillotina.directives import index


class INews(IItem):

    index('text', type='text')
    text = schema.Text(
        title=_('Text'),
        required=False)


@configure.contenttype(
    type_name='News',
    schema=INews,
    behaviors=['guillotina.behaviors.dublincore.IDublinCore'],
    allowed_types=[]  # dynamically calculated
)
class News(Item):
    pass
