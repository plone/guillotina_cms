from guillotina import configure
from guillotina.behaviors.instance import ContextBehavior
from guillotina_cms.interfaces import IBlocks
from guillotina_cms.interfaces import IBlocksMarker
from guillotina_cms.interfaces import IGutenberg
from guillotina_cms.interfaces import IGutenbergMarker
from guillotina_cms.interfaces import IRichText
from guillotina_cms.interfaces import IRichTextMarker


@configure.behavior(
    title="Blocks behavior",
    provides=IBlocks,
    marker=IBlocksMarker,
    for_="guillotina.interfaces.IResource",
)
class Blocks(ContextBehavior):
    pass


@configure.behavior(
    title="Gutenberg behavior",
    marker=IGutenbergMarker,
    provides=IGutenberg,
    for_="guillotina.interfaces.IResource",
)
class Gutenberg(ContextBehavior):
    pass


@configure.behavior(
    title="RichText behavior",
    marker=IRichTextMarker,
    provides=IRichText,
    for_="guillotina.interfaces.IResource",
)
class RichText(ContextBehavior):
    pass
