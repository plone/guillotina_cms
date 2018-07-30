# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Folder
from guillotina.directives import index
from guillotina_cms.interfaces import IDocument


@configure.contenttype(
    type_name='Document',
    schema=IDocument,
    behaviors=[
        'guillotina.behaviors.dublincore.IDublinCore',
        'guillotina_cms.interfaces.base.ICMSBehavior'],
    allowed_types=[]  # dynamically calculated
)
class Document(Folder):
    pass


@index.with_accessor(IDocument, 'text', type='searchabletext')
def get_text_from_richtext(ob):
    # Richtext is a dict and we only care about the text
    if ob.text is not None:
        return ob.text.data
