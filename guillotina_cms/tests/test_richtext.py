import json
import os

import pytest


pytestmark = pytest.mark.skipif(
    os.environ.get('DATABASE') not in ('postgresql', 'cockroachdb'),
    reason="These tests are only for postgresql")


async def test_li(cms_requester):
    async with cms_requester as requester:

        resp1, status = await requester(
            'POST',
            '/db/guillotina/',
            data=json.dumps({
                '@type': 'Document',
                'title': 'Document 1',
                'id': 'doc1'
            })
        )
        assert status == 201

        resp2, status = await requester(
            'POST',
            '/db/guillotina/',
            data=json.dumps({
                '@type': 'Document',
                'title': 'Document 2',
                'id': 'doc2',
                'text': {
                    'content-type': 'text/html',
                    'encoding': 'utf-8',
                    'data': '''
                    <p>
                    <a href="@resolveuid/{}">foobar</a>
                    </p>
                    '''.format(resp1['@uid'])
                }
            })
        )
        assert status == 201

        resp, status = await requester(
            'GET', '/db/guillotina/doc2/@links')
        assert resp1['@uid'] in resp
        resp, status = await requester(
            'GET', '/db/guillotina/doc1/@links-to')
        assert resp2['@uid'] in resp


async def test_links_translated(cms_requester):
    async with cms_requester as requester:

        resp1, status = await requester(
            'POST',
            '/db/guillotina/',
            data=json.dumps({
                '@type': 'Document',
                'title': 'Document 1',
                'id': 'doc1'
            })
        )
        assert status == 201

        resp2, status = await requester(
            'POST',
            '/db/guillotina/',
            data=json.dumps({
                '@type': 'Document',
                'title': 'Document 2',
                'id': 'doc2',
                'text': {
                    'content-type': 'text/html',
                    'encoding': 'utf-8',
                    'data': '''
                    <p>
                    <a href="@resolveuid/{}">foobar</a>
                    </p>
                    '''.format(resp1['@uid'])
                }
            })
        )
        assert status == 201

        resp, status = await requester('GET', '/db/guillotina/doc2')
        assert '/db/guillotina/doc1' in resp['text']['data']
