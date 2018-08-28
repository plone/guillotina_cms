from guillotina import configure
from guillotina.interfaces import IBeforeFieldModifiedEvent
from guillotina.interfaces import IObjectModifiedEvent
from guillotina.interfaces import IResource
from guillotina.interfaces import IBehavior

from guillotina_cms.interfaces import IVersioningMarker
from guillotina_cms.interfaces import IVersioning
from guillotina_cms.interfaces import IDiffCalculator


@configure.subscriber(for_=(IBeforeFieldModifiedEvent))
async def field_modified(event):
    if IBehavior.providedBy(event.field.context):
        context = event.field.context.context
    else:
        context = event.field.context

    if IVersioningMarker.providedBy(context):
        # its enabled to copy the diff
        diff_calculator = IDiffCalculator(event.field)
        orig_value = await event.field.async_get()
        diff_value = diff_calculator(orig_value, event.value)

        behavior = None
        if IBehavior.providedBy(event.field.context):
            behavior = [x for x in event.field.context.__implemented__][0].__identifier__

        diff = {
            'f': event.field.__name__,
            'b': behavior,
            'd': diff_value
        }

        temp_versions = getattr(context, '_v_temporal_versioning', [])
        temp_versions.append(diff)
        context._v_temporal_versioning = temp_versions


@configure.subscriber(for_=(IResource, IObjectModifiedEvent))
async def object_modified(object, event):
    if IVersioningMarker.providedBy(object):
        version_behavior = IVersioning(object)
        await version_behavior.load(create=True)
        version_behavior.diffs.append(object._v_temporal_versioning)
        version_behavior._p_register()
        del object._v_temporal_versioning
