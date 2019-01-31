from guillotina import configure
from guillotina.api.service import Service
from guillotina.api.content import resolve_uid
from guillotina.catalog import index
from guillotina.interfaces import IAsyncContainer
from guillotina.interfaces import IContainer
from guillotina.response import HTTPBadRequest
from guillotina.response import HTTPPreconditionFailed
from guillotina.transactions import get_transaction
from guillotina.utils import get_behavior

from guillotina_cms.interfaces import ICMSBehavior
from guillotina_cms.ordering import supports_ordering


@configure.service(
    method='GET', name="resolveuid/{uid}", context=IContainer,
    permission='guillotina.AccessContent',
    summary='Get content by UID',
    responses={
        "200": {
            "description": "Successful"
        }
    })
async def plone_resolve_uid(context, request):
    '''
    b/w compatible plone endpoint name
    '''
    return await resolve_uid(context, request)


MAX_FOLDER_SORT_SIZE = 5000


@configure.service(
    context=IAsyncContainer, method='PATCH',
    permission='guillotina.ModifyContent', name='@order')
class OrderContent(Service):
    order = None
    mapped = None
    subset_ids = None
    obj_id = None
    delta = None

    def __init__(self, context, request):
        super().__init__(context, request)
        self.order = []
        self.mapped = {}

    async def validate(self):
        # verify current order matches
        txn = get_transaction()
        if not supports_ordering(txn.storage):
            raise HTTPBadRequest(content={
                'message': 'Content ordering not supported'
            })

        conn = await txn.get_connection()
        results = await conn.fetch('''
    select id, (json->>'position_in_parent')::int as pos from {}
    WHERE parent_id = $1 AND of IS NULL
    ORDER BY (json->>'position_in_parent')::int ASC
    limit {}'''.format(
            txn.storage._objects_table_name, MAX_FOLDER_SORT_SIZE), self.context._p_oid)
        if len(results) >= MAX_FOLDER_SORT_SIZE:
            raise HTTPPreconditionFailed(content={
                'message': 'Content ordering not supported on folders larger than {}'.format(
                    MAX_FOLDER_SORT_SIZE
                )
            })

        results.sort(key=lambda item: item['pos'] or 0)
        for item in results:
            self.order.append(item['id'])
            self.mapped[item['id']] = item['pos']

        if len(self.subset_ids) > len(self.order):
            raise HTTPPreconditionFailed(content={
                'message': 'Invalid subset. More values than current ordering'
            })
        if len(self.subset_ids) == len(self.order):
            if self.subset_ids != self.order:
                raise HTTPPreconditionFailed(content={
                    'message': 'Invalid subset',
                    'current': self.order
                })
        else:
            # verify subset
            # find current ordered subset
            try:
                start = self.order.index(self.subset_ids[0])
                end = self.order.index(self.subset_ids[-1]) + 1
            except ValueError:
                raise HTTPPreconditionFailed(content={
                    'message': 'Invalid subset. Could not calculate subset match',

                })
            order_subset = self.order[start:end]
            if self.subset_ids != order_subset:
                raise HTTPPreconditionFailed(content={
                    'message': 'Invalid subset',
                    'current': order_subset
                })

        if ((self.order.index(self.obj_id) + self.delta + 1) > len(self.order) or (
                self.order.index(self.obj_id) + self.delta) < 0):
            raise HTTPPreconditionFailed(content={
                'message': 'Can not move. Invalid move target.'
            })

    async def swap(self, two):
        one = self.obj_id
        one_pos = self.mapped[one]
        two_pos = self.mapped[two]

        ob_one = await self.context.async_get(one)
        ob_two = await self.context.async_get(two)

        beh_one = await get_behavior(ob_one, ICMSBehavior)
        beh_two = await get_behavior(ob_two, ICMSBehavior)

        beh_one.position_in_parent = two_pos
        beh_two.position_in_parent = one_pos

        one_idx = self.order.index(one)
        two_idx = self.order.index(two)
        self.order[two_idx], self.order[one_idx] = self.order[one_idx], self.order[two_idx]

        await index.index_object(ob_one, indexes=['position_in_parent'], modified=True)
        await index.index_object(ob_two, indexes=['position_in_parent'], modified=True)
        return {
            one: {
                'idx': two_idx,
                'pos': two_pos
            },
            two: {
                'idx': one_idx,
                'pos': one_pos
            }
        }

    async def __call__(self):
        data = await self.request.json()
        self.subset_ids = data['subset_ids']
        self.obj_id = data['obj_id']
        self.delta = data['delta']

        await self.validate()

        # now swap position for item
        moved_item_index = self.order.index(self.obj_id)
        moved = {}
        # over range of delta and shift position of the rest the opposite direction
        # for example:
        #  - move idx 0, delta 3
        #    - idx 1, 2, 3 are moved to 0, 1, 2
        #  - move idx 4, delta -2
        #    - idx 2, 3 are moved to 3, 4
        if self.delta < 0:
            group = [i for i in reversed(
                self.order[moved_item_index + self.delta:moved_item_index + 1])]
        else:
            group = self.order[moved_item_index:moved_item_index + self.delta + 1]

        for item_id in group[1:]:
            moved.update(await self.swap(item_id))

        return moved
