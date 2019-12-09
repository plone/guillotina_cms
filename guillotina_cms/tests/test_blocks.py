from guillotina.tests.utils import create_content
from guillotina.content import Resource
from guillotina_cms.interfaces import IBlocks
from guillotina_cms.behaviors.editors import Blocks
import asyncio
import pytest
import json

pytestmark = pytest.mark.asyncio


async def test_default_blocks_layout(cms_requester):
    async with cms_requester as requester:
        # now test it...
        response, status = await requester("GET", "/db/guillotina/")
        assert (
            len(
                response["guillotina_cms.interfaces.blocks.IBlocks"]["blocks_layout"][
                    "items"
                ]
            )
            == 2
        )
        assert "tile1" in response["guillotina_cms.interfaces.blocks.IBlocks"]["blocks"]


async def test_blocks_endpoint_gives_us_registered_blocks(cms_requester):
    async with cms_requester as requester:
        # now test it...
        response, status = await requester("GET", "/db/guillotina/@blocks")
        assert status == 200
        assert len(response) >= 1
        assert "@blocks/" in response[0]["@id"]

        response, status = await requester("GET", "/db/guillotina/@blocks/title")
        assert status == 200
        assert response["type"] == "object"


async def test_conversation_behavior_returns_instance(dummy_request):
    ob = create_content(Resource)
    behavior = IBlocks(ob)
    assert isinstance(behavior, Blocks)


async def test_storing_blocks_behavior_data(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps(
                {
                    "@type": "Folder",
                    "title": "foobar",
                    "id": "foobar",
                    "@behaviors": ["guillotina_cms.interfaces.blocks.IBlocks"],
                    "guillotina_cms.interfaces.blocks.IBlocks": {
                        "blocks_layout": {"cols": ["#title-1", "#description-1"]},
                        "blocks": {"#title-1": {"@type": "title"}},
                    },
                }
            ),
        )
        assert status == 201

        resp, status = await requester("GET", "/db/guillotina/foobar")
        assert status == 200
        assert "guillotina_cms.interfaces.blocks.IBlocks" in resp
        assert "blocks_layout" in resp["guillotina_cms.interfaces.blocks.IBlocks"]
