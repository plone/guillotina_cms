from guillotina import configure
from guillotina.interfaces import IApplicationInitializedEvent
from guillotina.interfaces import IResourceFactory
from guillotina.component import get_utility
from guillotina.behaviors.dublincore import IDublinCore
from guillotina_cms.interfaces.base import ICMSBehavior
from guillotina_cms.interfaces.blocks import IBlocks
from guillotina.content import load_cached_schema


@configure.subscriber(for_=IApplicationInitializedEvent)
async def app_initialized(event):
    factory = get_utility(IResourceFactory, "Container")
    # factory = get_cached_factory("Container")
    factory.behaviors = (IDublinCore, ICMSBehavior, IBlocks)
    load_cached_schema()
