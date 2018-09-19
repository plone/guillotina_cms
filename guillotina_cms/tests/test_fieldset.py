
async def test_fieldset(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'GET',
            '/db/guillotina/@types/Document'
        )
        assert len(resp['fieldsets']) == 5

        for fieldset in resp['fieldsets']:
            if fieldset['title'] == 'default':
                assert len(fieldset['fields']) == 3

        resp, status = await requester(
            'GET',
            '/db/guillotina/@types/Document'
        )
        assert len(resp['fieldsets']) == 5

        for fieldset in resp['fieldsets']:
            if fieldset['title'] == 'default':
                assert len(fieldset['fields']) == 3
