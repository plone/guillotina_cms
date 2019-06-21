# -*- coding: utf-8 -*-
from guillotina import configure
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina.behaviors.properties import FunctionProperty
from guillotina.interfaces import IResource
from guillotina.utils import get_authenticated_user_id
from guillotina_cms.interfaces import IFollowing
from guillotina_cms.interfaces import IFollowingMarker


@configure.behavior(
    title="Following",
    provides=IFollowing,
    marker=IFollowingMarker,
    for_=IResource)
class Following(AnnotationBehavior):
    __local__properties__ = ('favorite',)

    def get_favorite(self):
        user = get_authenticated_user_id()
        return user in (self.favorites or [])

    def set_favorite(self, value):
        pass

    favorite = FunctionProperty(
        'favorite', get_favorite, set_favorite)
