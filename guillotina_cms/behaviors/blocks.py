from guillotina import configure
from guillotina.behaviors.instance import ContextBehavior
from guillotina_cms.interfaces import IBlocks


@configure.behavior(title="Blocks behavior", provides=IBlocks, for_="guillotina.interfaces.IResource")
class Blocks(ContextBehavior):
    pass
