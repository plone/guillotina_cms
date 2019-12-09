import json


async def test_menu_definition(cms_requester):
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

async def test_logo(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'GET',
            '/db/guillotina/@registry/guillotina_cms.interfaces.registry.IMenu.logo'
        )
        assert 'data:image/png;base64,' in resp['value'] 

        resp, status = await requester(
            'PATCH',
            '/db/guillotina/@registry/guillotina_cms.interfaces.registry.IMenu.logo',
            data=json.dumps({
                'value': "Image1"
            })
        )

        resp, status = await requester(
            'GET',
            '/db/guillotina/@logo'
        )
        assert status == 200

        assert 'Image1' in resp['value']