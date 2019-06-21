import asyncio
import json
import os

import aiohttp
import pytest
from diff_match_patch import diff_match_patch
from guillotina.testing import ADMIN_TOKEN


RECEIVED = None
dmp = diff_match_patch()


async def await_for_value(url):
    global RECEIVED
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(
                url,
                headers={'AUTHORIZATION': 'Basic %s' % ADMIN_TOKEN}) as ws:
            msg = await ws.receive()
            RECEIVED = msg


pytest.mark.skipif(os.environ.get('DATABASE') == 'postgresql',
                   reason="Flaky pg test")
async def _test_ws_edit(pubsub):
    async with pubsub as requester:
        resp, status = await requester(
            'POST',
            '/db/guillotina',
            data=json.dumps({
                '@type': 'Item',
                'title': 'item',
            })
        )
        url = pubsub.guillotina.server.make_url('db/guillotina/item/@ws-edit')
        asyncio.ensure_future(await_for_value(url))
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(
                    url,
                    headers={'AUTHORIZATION': 'Basic %s' % ADMIN_TOKEN}) as ws:
                # we should check version
                sending = {
                    't': 'dmp',
                    'f': 'title',
                    'v': dmp.patch_toText(dmp.patch_make(
                        'foobar', 'flub barsh dsfksld'))
                }
                await ws.send_str(json.dumps(sending))
                await asyncio.sleep(4)
                assert 'barsh' in json.loads(RECEIVED.data)['v']
