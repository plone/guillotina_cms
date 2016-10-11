# -*- coding: utf-8 -*-
from plone.server.addons import Addon
from plone.server.registry import ILayers

CMS_LAYER = 'pserver.cms.interfaces.ICMSLayer'


class CMSAddon(Addon):

    @classmethod
    def install(self, request):
        registry = request.site_settings
        registry.forInterface(ILayers).active_layers |= {
            CMS_LAYER
        }

    @classmethod
    def uninstall(self, request):
        registry = request.site_settings
        registry.forInterface(ILayers).active_layers -= {
            CMS_LAYER
        }
