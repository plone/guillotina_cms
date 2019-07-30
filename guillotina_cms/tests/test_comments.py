import json
import pytest


@pytest.mark.app_settings({"allow_discussion_types": ["Document"], "default_allow_discussion": True})
async def test_comments(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({"@type": "Document", "title": "Document 1", "id": "doc1"}),
        )

        resp, status = await requester("GET", "/db/guillotina/doc1/@comments")
        assert len(resp["items"]) == 0
        assert status == 200

        resp, status = await requester(
            "POST", "/db/guillotina/doc1/@comments", data=json.dumps({"text": "My text"})
        )
        assert status == 204

        resp, status = await requester("GET", "/db/guillotina/doc1/@comments")
        assert len(resp["items"]) == 1
        assert status == 200

        comment_id = resp["items"][0]["comment_id"]

        resp, status = await requester(
            "POST", "/db/guillotina/doc1/@comments/" + comment_id, data=json.dumps({"text": "My text"})
        )
        assert status == 204

        resp, status = await requester("GET", "/db/guillotina/doc1/@comments")
        assert len(resp["items"]) == 2
        assert status == 200

        resp, status = await requester(
            "PATCH", "/db/guillotina/doc1/@comments/" + comment_id, data=json.dumps({"text": "My text2"})
        )
        assert status == 204

        resp, status = await requester("GET", "/db/guillotina/doc1/@comments")
        assert len(resp["items"]) == 2
        assert resp["items"][0]["text"]["data"] == "My text2"
        assert status == 200

        resp, status = await requester("DELETE", "/db/guillotina/doc1/@comments/" + comment_id)
        assert status == 204

        resp, status = await requester("GET", "/db/guillotina/doc1/@comments")
        assert len(resp["items"]) == 0
        assert status == 200
