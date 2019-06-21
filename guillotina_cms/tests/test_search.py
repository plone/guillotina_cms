import os

import pytest
from guillotina_cms.tests.utils import add_content


@pytest.mark.skipif(os.environ.get('DATABASE', 'DUMMY') in ('cockroachdb', 'DUMMY'),
                    reason='Not for dummy db')
async def test_search(cms_requester):
    async with cms_requester as requester:
        await add_content(requester)
        # Make sure ES is fully sync
        # @search?path_starts=folder&depth_gte=2
        resp, status = await requester(
            'GET',
            '/db/guillotina/@search?path__starts=cms-folder0&depth__gte=1'
        )
        # Folder included
        assert resp['items_total'] == 11

        resp, status = await requester(
            'GET',
            '/db/guillotina/@search?path__starts=cms-folder0&depth__gte=2'
        )
        assert resp['items_total'] == 10

        resp, status = await requester(
            'GET',
            '/db/guillotina/@search?text__in=needs&portal_type=Document&_size=30'
        )
        assert resp['items_total'] == 20
