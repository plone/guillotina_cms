# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Item
from guillotina_cms.interfaces import INews
from guillotina.directives import index


@configure.contenttype(
    type_name='News',
    schema=INews,
    behaviors=[
        'guillotina.behaviors.dublincore.IDublinCore',
        'guillotina_cms.interfaces.base.ICMSBehavior',
        'guillotina_cms.interfaces.tiles.ITiles'],
    allowed_types=['Image', 'File']  # dynamically calculated
)
class News(Item):
    pass


@index.with_accessor(INews, 'text', type='searchabletext')
def get_text_from_richtext(ob):
    # Richtext is a dict and we only care about the text
    if ob.text is not None:
        return ob.text.data
