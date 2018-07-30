import asyncio
from guillotina_cms.tests.utils import add_content


async def test_search(cms_requester):
    async with cms_requester as requester:
        total = await add_content(requester)
        await asyncio.sleep(1)
        # Make sure ES is fully sync
        # @search?path_starts=folder&depth_gte=2
        resp, status = await requester(
            'GET',
            '/db/guillotina/@search?path__starts=cms-folder0&depth__gte=2'
        )
        # Folder included
        assert resp['items_total'] == 11

        resp, status = await requester(
            'GET',
            '/db/guillotina/@search?path__starts=cms-folder0&depth__gte=3'
        )
        assert resp['items_total'] == 10

        resp, status = await requester(
            'GET',
            '/db/guillotina/@search?text__in=needs&portal_type=Document&_size=30'
        )
        assert resp['items_total'] == 20

        # @search?title_in=lorem&portal_type=Document&review_state=published&_aggregations=portal_type+review_state

        resp, status = await requester(
            'GET',
            '/db/guillotina/@search?title__in=Document&portal_type=Document&review_state=private&_aggregations=portal_type+review_state&_size=30'
        )
        assert resp['aggregations']['type_name'][0]['key'] == 'Document'
        assert resp['aggregations']['type_name'][0]['doc_count'] == 20
