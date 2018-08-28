from guillotina import configure
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina.interfaces import IFileCleanup
from guillotina.interfaces import IResource
from guillotina_cms.interfaces import IVersioning
from guillotina_cms.interfaces import IVersioningMarker


import logging


logger = logging.getLogger('guillotina_versioning')


@configure.adapter(
    for_=IResource,
    provides=IFileCleanup)
class VersioningFileCleanup:
    def __init__(self, context):
        self.context = context

    def should_clean(self, **kwargs):
        if 'field' not in kwargs:
            return True
        if kwargs['field'].__name__ not in ('file', 'version_file'):
            return True
        if IVersioning.providedBy(self.context):
            return False
        return True


@configure.behavior(
    title="Versioning",
    provides=IVersioning,
    marker=IVersioningMarker,
    for_=IResource)
class Versioning(AnnotationBehavior):
    auto_serialize = False
    __annotations_data_key__ = 'metadata'
