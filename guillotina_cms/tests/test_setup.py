import asyncio
from guillotina_cms.tests.utils import add_content


async def test_basic_content(cms_requester):
    async with cms_requester as requester:
        await add_content(requester)
        await asyncio.sleep(1)
