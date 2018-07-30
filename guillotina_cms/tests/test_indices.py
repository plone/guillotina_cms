async def test_indices(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'GET',
            '/db/guillotina/@indices'
        )
        assert 'Item' in resp['types']
        assert 'title' in resp['types']['Item']
        assert 'text' in resp['types']['Item']['title']

        assert 'guillotina.behaviors.dublincore.IDublinCore' in resp['behaviors']  # noqa
        assert 'tags' in resp['behaviors']['guillotina.behaviors.dublincore.IDublinCore']  # noqa
        assert 'keyword' in resp['behaviors']['guillotina.behaviors.dublincore.IDublinCore']['tags']  # noqa