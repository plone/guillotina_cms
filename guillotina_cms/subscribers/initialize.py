from guillotina import configure
from guillotina.interfaces import IApplicationInitializedEvent
from guillotina.behaviors.dublincore import IDublinCore
from guillotina_cms.interfaces.base import ICMSBehavior
from guillotina_cms.interfaces.tiles import ITiles
from guillotina.content import get_cached_factory


@configure.subscriber(for_=IApplicationInitializedEvent)
async def app_initialized(event):
    factory = get_cached_factory("Container")
    factory.behaviors = (IDublinCore, ICMSBehavior, ITiles)
