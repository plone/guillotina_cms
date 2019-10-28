from guillotina import configure
from guillotina.behaviors.instance import ContextBehavior
from guillotina_cms.interfaces import ITiles
from guillotina_cms.interfaces import ITilesMarker
from guillotina_cms.interfaces import IGutenberg
from guillotina_cms.interfaces import IGutenbergMarker
from guillotina_cms.interfaces import IRichText
from guillotina_cms.interfaces import IRichTextMarker


@configure.behavior(
    title="Tiles behavior",
    provides=ITiles,
    marker=ITilesMarker,
    for_="guillotina.interfaces.IResource",
)
class Tiles(ContextBehavior):
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
