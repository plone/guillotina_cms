import json


async def test_menu(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'PATCH',
            '/db/guillotina/@registry/guillotina_cms.interfaces.registry.IMenu.definition',
            data=json.dumps({
                'value': ['option1', 'option2']
            })
        )

        resp, status = await requester(
            'GET',
            '/db/guillotina/@registry/'
        )

        resp, status = await requester(
            'GET',
            '/db/guillotina/@menu'
        )
        assert status == 200

        assert 'option1' in resp['value']