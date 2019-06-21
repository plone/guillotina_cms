# -*- coding: utf-8 -*-
from guillotina import configure
from guillotina.addons import Addon
from guillotina.interfaces import ILayers
from guillotina.utils import get_registry
from guillotina_cms.behaviors.image import IImageAttachment
from guillotina_cms.behaviors.syndication import ISyndicationSettings
from guillotina_cms.interfaces import ICMSBehavior
from guillotina_cms.interfaces import IImagingSettings


CMS_LAYER = 'guillotina_cms.interfaces.ICMSLayer'


@configure.addon(
    name='cms',
    title='Guillotina CMS')
class CMSAddon(Addon):

    @classmethod
    async def install(cls, container, request):
        container.add_behavior(ISyndicationSettings)
        container.add_behavior(IImageAttachment)
        container.add_behavior(ICMSBehavior)

        registry = await get_registry()
        registry.for_interface(ILayers)['active_layers'] |= {
            CMS_LAYER
        }
        registry.register_interface(IImagingSettings)
        registry.register()

    @classmethod
    async def uninstall(cls, container, request):
        container.remove_behavior(ISyndicationSettings)
        registry = await get_registry()
        registry.for_interface(ILayers)['active_layers'] -= {
            CMS_LAYER
        }
        registry.register()
