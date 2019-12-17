import json
import pytest

pytestmark = pytest.mark.asyncio


async def test_css_definition(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'PATCH',
            '/db/guillotina/@registry/guillotina_cms.interfaces.registry.ICustomTheme.css',
            data=json.dumps({
                'value': "body { color: red }"
            })
        )

        resp, status = await requester(
            'GET',
            '/db/guillotina/@css'
        )
        assert status == 200

        assert b'color: red' in resp