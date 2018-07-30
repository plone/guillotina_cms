
from guillotina import configure
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina_cms.interfaces import ITiles


@configure.behavior(
    title="Tiles behavior",
    provides=ITiles,
    for_="guillotina.interfaces.IResource")
class Tiles(AnnotationBehavior):
    __annotations_data_key__ = 'itiles'
