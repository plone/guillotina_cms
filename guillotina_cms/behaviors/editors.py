from guillotina import configure
from guillotina.behaviors.instance import ContextBehavior
from guillotina_cms.interfaces import IBlocks
from guillotina_cms.interfaces import IGutenberg
from guillotina_cms.interfaces import IRichText
from guillotina_cms.interfaces import IReactPageLayout
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


@configure.behavior(
    title="React Page behavior",
    provides=IReactPageLayout,
    for_="guillotina.interfaces.IResource",
)

class ReactPage(ContextBehavior):
    pass


def get_text(layout, result):
    if isinstance(layout, dict):
        for key, value in layout.items():
            if key == 'text':
                result['text'] += f" {value}"
            if isinstance(value, dict) or isinstance(value, list):
                get_text(value, result)
    if isinstance(layout, list):
        for value in layout:
            get_text(value, result)


@index.with_accessor(IReactPageLayout, "text", type="searchabletext")
def get_text_from_react_page_layout(ob):
    # ReactPageLayout is a json that needs to be parsed to extract text
    if ob.layout is not None:
        result = {
            'text': ''
        }
        get_text(ob.layout, result)
        return result['text']
