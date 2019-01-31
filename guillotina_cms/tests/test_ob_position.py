import json
import os

import pytest
from guillotina.tests import utils

from guillotina_cms.interfaces import ICMSBehavior
from guillotina_cms.ordering import get_last_child_position


@pytest.mark.skipif(os.environ.get('DATABASE', 'DUMMY') in ('cockroachdb', 'DUMMY'),
                    reason='Not for dummy db')
async def test_get_max_position_in_folder(cms_requester):
    async with cms_requester as requester:
        await requester(
            'POST', '/db/guillotina/',
            data=json.dumps({
                "@type": "Item",
                "title": "Item1",
                "id": "item1",
                "@behaviors": [ICMSBehavior.__identifier__]
            })
        )
        await requester(
            'POST', '/db/guillotina/',
            data=json.dumps({
                "@type": "Item",
                "title": "Item2",
                "id": "item2",
                "@behaviors": [ICMSBehavior.__identifier__]
            })
        )

        request = utils.get_mocked_request(requester.db)
        root = await utils.get_root(request)
        container = await root.async_get('guillotina')
        pos = await get_last_child_position(container)
        assert pos > 1

        resp1, status = await requester('GET', '/db/guillotina/item1')
        resp2, status = await requester('GET', '/db/guillotina/item2')
        assert (resp2[ICMSBehavior.__identifier__]['position_in_parent'] >  # noqa
                resp1[ICMSBehavior.__identifier__]['position_in_parent'])


@pytest.mark.skipif(os.environ.get('DATABASE', 'DUMMY') in ('cockroachdb', 'DUMMY'),
                    reason='Not for dummy db')
async def test_move_item_up(cms_requester):
    async with cms_requester as requester:
        for idx in range(10):
            await requester(
                'POST', '/db/guillotina/',
                data=json.dumps({
                    "@type": "Item",
                    "title": "Item {}".format(idx),
                    "id": "item{}".format(idx),
                    "@behaviors": [ICMSBehavior.__identifier__]
                })
            )

        resp, status = await requester('GET', '/db/guillotina/item9')
        assert resp[ICMSBehavior.__identifier__]['position_in_parent'] >= 9

        resp, status = await requester(
            'PATCH', '/db/guillotina/@order',
            data=json.dumps({
                "subset_ids": ['item0', 'item1', 'item2', 'item3'],
                "obj_id": "item1",
                "delta": 1
            })
        )
        assert status == 200
        assert resp['item1']['idx'] == 2
        assert resp['item2']['idx'] == 1

        resp1, status = await requester('GET', '/db/guillotina/item1')
        assert resp1[ICMSBehavior.__identifier__]['position_in_parent'] == resp['item1']['pos']
        resp2, status = await requester('GET', '/db/guillotina/item2')
        assert resp2[ICMSBehavior.__identifier__]['position_in_parent'] == resp['item2']['pos']

        resp, status = await requester(
            'PATCH', '/db/guillotina/@order',
            data=json.dumps({
                "subset_ids": ['item6', 'item7', 'item8', 'item9'],
                "obj_id": "item9",
                "delta": 1
            })
        )
        assert status == 412

        resp, status = await requester(
            'PATCH', '/db/guillotina/@order',
            data=json.dumps({
                "subset_ids": ['item0', 'item2', 'item1', 'item3'],
                "obj_id": "item0",
                "delta": 3
            })
        )
        assert status == 200
        assert len(resp) == 4
        assert resp['item0']['idx'] == 3
        assert resp['item2']['idx'] == 0
        assert resp['item1']['idx'] == 1
        assert resp['item3']['idx'] == 2


@pytest.mark.skipif(os.environ.get('DATABASE', 'DUMMY') in ('cockroachdb', 'DUMMY'),
                    reason='Not for dummy db')
async def test_move_item_down(cms_requester):
    async with cms_requester as requester:
        for idx in range(10):
            await requester(
                'POST', '/db/guillotina/',
                data=json.dumps({
                    "@type": "Item",
                    "title": "Item {}".format(idx),
                    "id": "item{}".format(idx),
                    "@behaviors": [ICMSBehavior.__identifier__]
                })
            )

        resp1, status = await requester('GET', '/db/guillotina/item8')
        resp2, status = await requester('GET', '/db/guillotina/item9')
        assert (resp2[ICMSBehavior.__identifier__]['position_in_parent'] >  # noqa
                resp1[ICMSBehavior.__identifier__]['position_in_parent'])

        resp, status = await requester(
            'PATCH', '/db/guillotina/@order',
            data=json.dumps({
                "subset_ids": ['item0', 'item1', 'item2', 'item3'],
                "obj_id": "item2",
                "delta": -1
            })
        )
        assert status == 200
        assert resp['item2']['idx'] == 1
        assert resp['item1']['idx'] == 2

        resp1, status = await requester('GET', '/db/guillotina/item1')
        assert resp1[ICMSBehavior.__identifier__]['position_in_parent'] == resp['item1']['pos']
        resp2, status = await requester('GET', '/db/guillotina/item2')
        assert resp2[ICMSBehavior.__identifier__]['position_in_parent'] == resp['item2']['pos']

        resp, status = await requester(
            'PATCH', '/db/guillotina/@order',
            data=json.dumps({
                "subset_ids": ['item0', 'item1', 'item2', 'item3'],
                "obj_id": "item0",
                "delta": -1
            })
        )
        assert status == 412

        resp, status = await requester(
            'PATCH', '/db/guillotina/@order',
            data=json.dumps({
                "subset_ids": ['item0', 'item2', 'item1', 'item3'],
                "obj_id": "item3",
                "delta": -3
            })
        )
        assert status == 200
        assert len(resp) == 4
        assert resp['item3']['idx'] == 0
        assert resp['item0']['idx'] == 1
        assert resp['item2']['idx'] == 2
        assert resp['item1']['idx'] == 3
