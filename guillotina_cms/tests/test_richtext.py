import json

import pytest
from guillotina.tests.test_catalog import NOT_POSTGRES


@pytest.mark.app_settings({"applications": ["guillotina_linkintegrity"]})
@pytest.mark.skipif(NOT_POSTGRES, reason="Only PG")
async def test_li(cms_requester):
    async with cms_requester as requester:

        resp1, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({"@type": "Document", "title": "Document 1", "id": "doc1"}),
        )
        assert status == 201

        resp2, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps(
                {
                    "@type": "Document",
                    "@behaviors": ["guillotina_cms.interfaces.editors.IRichText"],
                    "title": "Document 2",
                    "id": "doc2",
                    "guillotina_cms.interfaces.editors.IRichText": {
                        "text": {
                            "encoding": "utf-8",
                            "content-type": "text/html",
                            "data": """
                    <p>
                    <a href="@resolveuid/{}">foobar</a>
                    </p>
                    """.format(
                            resp1["@uid"]
                        ),
                    },
                }}
            ),
        )
        assert status == 201

        resp, status = await requester("GET", "/db/guillotina/doc2/@links")
        assert resp1["@uid"] in resp
        resp, status = await requester("GET", "/db/guillotina/doc1/@links-to")
        assert resp2["@uid"] in resp


@pytest.mark.app_settings({"applications": ["guillotina_linkintegrity"]})
@pytest.mark.skipif(NOT_POSTGRES, reason="Only PG")
async def test_links_translated(cms_requester):
    async with cms_requester as requester:

        resp1, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({"@type": "Document", "title": "Document 1", "id": "doc1"}),
        )
        assert status == 201

        resp2, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps(
                {
                    "@type": "Document",
                    "@behaviors": ["guillotina_cms.interfaces.editors.IRichText"],
                    "title": "Document 2",
                    "id": "doc2",
                    "guillotina_cms.interfaces.editors.IRichText": {
                        "text": {
                            "encoding": "utf-8",
                            "content-type": "text/html",
                            "data": """
                    <p>
                    <a href="@resolveuid/{}">foobar</a>
                    </p>
                    """.format(
                            resp1["@uid"]
                        ),
                    },
                }}
            ),
        )
        assert status == 201

        resp, status = await requester("GET", "/db/guillotina/doc2")
        assert "/db/guillotina/doc1" in resp["guillotina_cms.interfaces.editors.IRichText"]["text"]["data"]
