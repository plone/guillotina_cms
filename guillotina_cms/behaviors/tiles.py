from guillotina import configure
from guillotina.behaviors.instance import ContextBehavior
from guillotina_cms.interfaces import ITiles


@configure.behavior(title="Tiles behavior", provides=ITiles, for_="guillotina.interfaces.IResource")
class Tiles(ContextBehavior):
    pass
