from guillotina import configure
from guillotina.interfaces import IResource
from guillotina_cms.interfaces import ICMSLayer
from guillotina.utils import get_behavior
from guillotina_cms.interfaces import ICMSBehavior
from guillotina.interfaces import IAbsoluteURL
from guillotina.component import getMultiAdapter
from guillotina.utils import get_current_container


@configure.service(
    context=IResource,
    layer=ICMSLayer,
    name="@history",
    method="GET",
    permission="guillotina.SeePermissions",
)
async def history(context, request):
    bhr = await get_behavior(context, ICMSBehavior)
    container = get_current_container()
    result = []
    context_url = getMultiAdapter((context, request), IAbsoluteURL)()
    container_url = getMultiAdapter((container, request), IAbsoluteURL)()
    for ident, hist_data in enumerate(bhr.history):
        actor = hist_data.get("actor", "")
        type_ = hist_data.get("type", "")
        title = hist_data.get("title", "")
        value = {
            "@id": f"{context_url}/@history/{ident}",
            "action": title,
            "comments": hist_data.get("comments", ""),
            "time": hist_data.get("time", ""),
            "transition_title": title,
            "type": type_,
            "actor": {
                "@id": f"{container_url}/@users/{actor}",
                "fullname": actor,
                "id": actor,
                "username": actor
            }
        }

        data = hist_data.get("data", {})
        if type_ == 'versioning':
            value['may_revert']: False
            value['version']: ident
        elif type_ == "workflow":
            value['state_title'] = data.get('review_state')
            value['review_state'] = data.get('review_state')
        result.append(value)
    return result
        
