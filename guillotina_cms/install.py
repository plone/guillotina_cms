# -*- coding: utf-8 -*-
from guillotina import configure
from guillotina.addons import Addon
from guillotina.interfaces import ILayers
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

        registry = request.container_settings
        registry.for_interface(ILayers)['active_layers'] |= {
            CMS_LAYER
        }
        registry.register_interface(IImagingSettings)
        registry._p_register()

    @classmethod
    def uninstall(cls, container, request):
        container.remove_behavior(ISyndicationSettings)
        registry = request.container_settings
        registry.for_interface(ILayers)['active_layers'] -= {
            CMS_LAYER
        }
        registry._p_register()
