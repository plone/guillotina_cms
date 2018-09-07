import json

async def test_history_creation(cms_requester):
    async with cms_requester as requester:

        resp, status = await requester(
            'POST',
            '/db/guillotina/',
            data=json.dumps({
                '@type': 'Document',
                'title': 'Document 1',
                'id': 'doc1'
            })
        )

        resp, status = await requester(
            'GET',
            '/db/guillotina/doc1'
        )

        assert resp['guillotina_cms.interfaces.base.ICMSBehavior']['history'] is not None
        assert resp['guillotina_cms.interfaces.base.ICMSBehavior']['history'][0]['title'] == 'Created'

        resp, status = await requester(
            'GET',
            '/db/guillotina/doc1/@workflow'
        )

        assert resp['history'] is not None
        assert resp['history'][0]['title'] == 'Created'
