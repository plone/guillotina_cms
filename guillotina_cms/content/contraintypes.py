from guillotina import configure
from guillotina.interfaces import IConstrainTypes
from zope.interface import Interface
from guillotina.constraintypes import FTIConstrainAllowedTypes


@configure.adapter(
    for_=Interface,
    provides=IConstrainTypes)
class CMSCustomAllowedTypes(FTIConstrainAllowedTypes):

    def get_allowed_types(self) -> list:
        tn = getattr(self.context, '__allowed_types__', None)
        if tn is not None:
            return tn
        else:
            return super(CMSCustomAllowedTypes, self).get_allowed_types()
