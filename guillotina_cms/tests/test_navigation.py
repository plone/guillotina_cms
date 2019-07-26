import json
import pytest
import os


@pytest.mark.skipif(
    os.environ.get("DATABASE", "DUMMY") in ("cockroachdb", "DUMMY"), reason="Not for dummy db"
)
async def test_navigation(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            "POST", "/db/guillotina/", data=json.dumps({"@type": "CMSFolder", "id": "folder1"})
        )
        resp, status = await requester(
            "POST", "/db/guillotina/folder1", data=json.dumps({"@type": "Document", "id": "doc1"})
        )
        resp, status = await requester(
            "POST", "/db/guillotina/folder1", data=json.dumps({"@type": "Document", "id": "doc2"})
        )

        resp, status = await requester("GET", "/db/guillotina/@navigation?expand.navigation.depth=2")

        assert len(resp["items"][0]["items"]) == 2
