from guillotina import configure
from guillotina.behaviors.instance import ContextBehavior
from guillotina_cms.interfaces import IBlocks
from guillotina_cms.interfaces import IGutenberg
from guillotina_cms.interfaces import IRichText
from guillotina.directives import index


@configure.behavior(
    title="Blocks behavior",
    provides=IBlocks,
    for_="guillotina.interfaces.IResource",
)
class Blocks(ContextBehavior):
    pass


@configure.behavior(
    title="Gutenberg behavior",
    provides=IGutenberg,
    for_="guillotina.interfaces.IResource",
)
class Gutenberg(ContextBehavior):
    pass



@index.with_accessor(IGutenberg, "gutenberg", type="searchabletext")
def get_text_from_gutenberg(ob):
    # Richtext is a dict and we only care about the text
    if ob.gutenberg is not None:
        return ob.gutenberg



@configure.behavior(
    title="RichText behavior",
    provides=IRichText,
    for_="guillotina.interfaces.IResource",
)
class RichText(ContextBehavior):
    pass


@index.with_accessor(IRichText, "text", type="searchabletext")
def get_text_from_richtext(ob):
    # Richtext is a dict and we only care about the text
    if ob.text is not None:
        return ob.text.data