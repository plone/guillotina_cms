from guillotina import configure
from guillotina.interfaces import IResource
from guillotina.interfaces import IObjectAddedEvent
from guillotina_cms.interfaces import ICMSBehavior
from guillotina_cms.interfaces import IWorkflow
from guillotina.component import query_adapter
from guillotina.utils import get_authenticated_user_id, get_current_request
from guillotina.security.utils import apply_sharing
import datetime


@configure.subscriber(for_=(IResource, IObjectAddedEvent))
async def cms_object_added(obj, event):
    cms = query_adapter(obj, ICMSBehavior)
    if cms is not None:
        request = get_current_request()
        user_id = get_authenticated_user_id(request)

        workflow = IWorkflow(obj)
        await cms.load(create=True)
        initial_state = workflow.initial_state

        await apply_sharing(obj, workflow.states[initial_state]['set_permission'])

        setattr(cms, 'history', [])
        cms.history.append(
            {
                'actor': user_id,
                'comments': '',
                'time': datetime.datetime.now(),
                'title': 'Created',
                'type': 'workflow',
                'data': {
                    'action': None,
                    'review_state': initial_state,
                }
            }
        )
        cms._p_register()
