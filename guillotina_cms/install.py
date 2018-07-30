# -*- coding: utf-8 -*-
from guillotina.addons import Addon
from guillotina.interfaces import ILayers
from guillotina import configure

CMS_LAYER = 'guillotina_cms.interfaces.ICMSLayer'


@configure.addon(
    name='cms',
    title='Guillotina CMS')
class CMSAddon(Addon):

    @classmethod
    async def install(cls, container, request):
        registry = request.container_settings
        registry.for_interface(ILayers)['active_layers'] |= {
            CMS_LAYER
        }
        registry._p_register()

    @classmethod
    def uninstall(cls, site, request):
        registry = request.container_settings
        registry.for_interface(ILayers)['active_layers'] -= {
            CMS_LAYER
        }
        registry._p_register()