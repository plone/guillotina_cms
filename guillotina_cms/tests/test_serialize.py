import json

from guillotina_cms.behaviors.syndication import ISyndicationSettings


async def test_behaviors(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'POST',
            '/db/guillotina',
            data=json.dumps({
                'id': 'doc1',
                '@type': 'Document'
            })
        )
        resp, status = await requester(
            'GET',
            '/db/guillotina/doc1/@behaviors'
        )
        assert status == 200
        result = resp[ISyndicationSettings.__identifier__]['properties']
        assert 'vocabulary' in result['sort_on']  # noqa
