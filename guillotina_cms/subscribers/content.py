import datetime

from guillotina import configure
from guillotina.catalog import index
from guillotina.component import query_adapter
from guillotina.interfaces import IObjectAddedEvent
from guillotina.interfaces import IResource
from guillotina.security.utils import apply_sharing
from guillotina.transactions import get_transaction
from guillotina.utils import get_authenticated_user_id
from guillotina_cms.interfaces import ICMSBehavior
from guillotina_cms.interfaces import IWorkflow
from guillotina_cms.ordering import get_next_order
from guillotina_cms.ordering import supports_ordering


@configure.subscriber(
    for_=(IResource, IObjectAddedEvent),
    priority=1001)  # after indexing
async def cms_object_added(obj, event):
    cms = query_adapter(obj, ICMSBehavior)
    if cms is not None:
        user_id = get_authenticated_user_id()

        workflow = IWorkflow(obj)
        await cms.load(create=True)
        state = cms.review_state

        if 'set_permission' in workflow.states[state]:
            await apply_sharing(obj, workflow.states[state]['set_permission'])

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
                    'review_state': state,
                }
            }
        )
        cms.register()
        txn = get_transaction()
        if supports_ordering(txn.storage):
            pos = await get_next_order()
            cms.position_in_parent = pos
            indexer = index.get_indexer()
            if indexer is None:
                return
            if obj.uuid not in indexer.index:
                indexer.index[obj.uuid] = {}
            indexer.index[obj.uuid]['position_in_parent'] = cms.position_in_parent

    if hasattr(obj, 'title') and obj.title is None:
        obj.title = obj.id
