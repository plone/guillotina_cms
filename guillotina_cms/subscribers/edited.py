from guillotina import configure
from guillotina.interfaces import IBeforeObjectModifiedEvent
from guillotina.interfaces import IObjectModifiedEvent
from guillotina.interfaces import IResource

from guillotina_cms.interfaces import IDiffCalculator
from guillotina_cms.interfaces import IVersioning
from guillotina_cms.interfaces import IVersioningMarker


@configure.subscriber(for_=(IBeforeObjectModifiedEvent))
async def before_object_modified(context, event):

    if IVersioningMarker.providedBy(context):
        # its enabled to copy the diff
        diff_calculator = IDiffCalculator(event.context, None)
        if diff_calculator is None:
            return
        context._v_temporal_versioning = await diff_calculator(event.payload)


@configure.subscriber(for_=(IResource, IObjectModifiedEvent))
async def object_modified(object, event):
    if IVersioningMarker.providedBy(object):
        version_behavior = IVersioning(object)
        await version_behavior.load(create=True)
        if hasattr(object, '_v_temporal_versioning'):
            version_behavior.diffs.append(object._v_temporal_versioning)
            version_behavior._p_register()
            del object._v_temporal_versioning
