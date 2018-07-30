from guillotina import configure
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina_cms.interfaces import IBlocks
from guillotina_cms.interfaces import IBlocksMarker


@configure.behavior(
    title="Blocks behavior",
    provides=IBlocks,
    marker=IBlocksMarker,
    for_="guillotina.interfaces.IResource")
class Blocks(AnnotationBehavior):
    pass
