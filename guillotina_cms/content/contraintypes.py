from guillotina import app_settings
from guillotina import configure
from guillotina import FACTORY_CACHE
from zope.interface import Interface
from guillotina.constraintypes import FTIConstrainAllowedTypes

from guillotina_cms.interfaces import ICMSConstrainTypes
from guillotina.interfaces import IConstrainTypes


@configure.adapter(for_=Interface, provides=ICMSConstrainTypes)
class CMSCustomAllowedTypes(FTIConstrainAllowedTypes):
    def get_allowed_types(self) -> list:
        tn = getattr(self.context, "__allowed_types__", None)
        if tn is None:
            tn = super(CMSCustomAllowedTypes, self).get_allowed_types()

        if tn is None:
            tn = FACTORY_CACHE.keys()
        global_disallowed_types = app_settings.get("global_disallowed_types", [])
        return [type_ for type_ in tn if type_ not in global_disallowed_types]



@configure.adapter(for_=Interface, provides=IConstrainTypes)
class CMSCustomAllowedTypes(FTIConstrainAllowedTypes):
    def get_allowed_types(self) -> list:
        tn = getattr(self.context, "__allowed_types__", None)
        if tn is None:
            tn = super(CMSCustomAllowedTypes, self).get_allowed_types()

        if tn is None:
            tn = FACTORY_CACHE.keys()
        return tn
