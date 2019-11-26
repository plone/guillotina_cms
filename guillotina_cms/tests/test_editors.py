import json
import pytest
import os

REACT_PAGE_PAYLOAD = {"id":"1","cells":[{"id":"5ac89ec4-7536-4120-a072-8eedad0a48ff","inline":None,"size":12,"rows":[{"id":"d813d094-215a-43ec-bcdd-d5fd6258b915","cells":[{"id":"3fde7b92-fbfe-4b2d-85b3-bad431939df6","inline":None,"size":12,"content":{"plugin":{"name":"ory/editor/core/content/slate","version":"0.0.3"},"state":{"serialized":{"object":"value","document":{"object":"document","data":{},"nodes":[{"object":"block","type":"HEADINGS/HEADING-ONE","data":{"align":"center"},"nodes":[{"object":"text","text":"The ORY Editor","marks":[]}]},{"object":"block","type":"PARAGRAPH/PARAGRAPH","data":{"align":"left"},"nodes":[{"object":"text","text":"","marks":[]},{"object":"inline","type":"LINK/LINK","data":{"href":"https://www.ory.sh/"},"nodes":[{"object":"text","text":"ORY","marks":[]}]},{"object":"text","text":" is a company building and maintaining developer tools for a safer, more accessible web. You might also like our other ","marks":[]},{"object":"inline","type":"LINK/LINK","data":{"href":"https://github.com/ory"},"nodes":[{"object":"text","text":"Open Source","marks":[]}]},{"object":"text","text":" tools! The ORY Editor is a smart, extensible and modern editor (\"WYSIWYG\") for the web written in React.","marks":[]}]},{"object":"block","type":"PARAGRAPH/PARAGRAPH","data":{"align":"left"},"nodes":[{"object":"text","text":"The ORY Editor was written because we urgently needed a robust and modern content editing solution for our open education platform ","marks":[]},{"object":"inline","type":"LINK/LINK","data":{"href":"https://en.serlo.org/serlo"},"nodes":[{"object":"text","text":"serlo.org","marks":[]}]},{"object":"text","text":". Serlo is the largest open education platform in Germany, works like the Wikipedia and is used by millions every year.","marks":[]}]}]}}}}}]},{"id":"c15959de-4767-41b7-9814-71626d6cbcdb","cells":[{"id":"33c58cda-94b5-4c2e-9232-9aa27a4aff8d","inline":None,"size":6,"content":{"plugin":{"name":"ory/editor/core/content/slate","version":"0.0.3"},"state":{"serialized":{"object":"value","document":{"object":"document","data":{},"nodes":[{"object":"block","type":"HEADINGS/HEADING-THREE","data":{"align":"left"},"nodes":[{"object":"text","text":"ORY Sites","marks":[]}]},{"object":"block","type":"PARAGRAPH/PARAGRAPH","data":{},"nodes":[{"object":"text","text":"ORY Sites is an ","marks":[]},{"object":"text","text":"next-gen","marks":[{"object":"mark","type":"EMPHASIZE/STRONG","data":{}}]},{"object":"text","text":" ","marks":[]},{"object":"text","text":"open source static site generator","marks":[{"object":"mark","type":"EMPHASIZE/STRONG","data":{}}]},{"object":"text","text":" based on the ORY Editor. Create stunning websites, write your own designs and plugins, and be done with databases, application servers, and security updates.","marks":[]}]},{"object":"block","type":"HEADINGS/HEADING-FIVE","data":{"align":"center"},"nodes":[{"object":"text","text":"","marks":[]},{"object":"inline","type":"LINK/LINK","data":{"href":"https://www.ory.sh/sites?utm_source=github&utm_medium=link&utm_campaign=editor_demo"},"nodes":[{"object":"text","text":"Learn more about ORY Sites!","marks":[]}]},{"object":"text","text":"","marks":[]}]},{"object":"block","type":"PARAGRAPH/PARAGRAPH","data":{},"nodes":[{"object":"text","text":"","marks":[]}]}]}}}}},{"id":"d5e4efbe-66f0-4344-9df0-f0720b5d1f5d","inline":None,"size":6,"content":{"plugin":{"name":"ory/sites/plugin/content/html5-video","version":"0.0.1"},"state":{"url":"images/app-preview.mp4"}}}]}]}]}  # noqa


@pytest.mark.skipif(
    os.environ.get("DATABASE", "DUMMY") in ("cockroachdb", "DUMMY"), reason="Not for dummy db"
)
@pytest.mark.app_settings(
    {
        "applications": ["guillotina.contrib.catalog.pg"],
        "load_utilities": {
            "catalog": {
                "provides": "guillotina.interfaces.ICatalogUtility",
                "factory": "guillotina.contrib.catalog.pg.PGSearchUtility",
            }
        },
    }
)
async def test_react_page(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({
                "@type": "Document",
                "@behaviors": ["guillotina_cms.interfaces.editors.IReactPageLayout"],
                "id": "doc1",
                "guillotina_cms.interfaces.editors.IReactPageLayout": {
                    "layout": REACT_PAGE_PAYLOAD
                }
            })
        )
        assert status == 201

        resp, status = await requester("GET", "/db/guillotina/@search?text__in=is+a+smart")
        assert len(resp['items']) == 1
