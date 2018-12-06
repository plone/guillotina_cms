import json


async def test_id_generator(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'POST',
            '/db/guillotina',
            data=json.dumps({
                '@type': 'Folder',
                'title': 'Folder 32!*&[]#',
            })
        )
        assert 'folder-32' in resp['@id']
