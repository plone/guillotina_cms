from guillotina.tests.utils import create_content
from guillotina.content import Resource
from guillotina_cms.interfaces import ITiles
from guillotina_cms.behaviors.tiles import Tiles

import json


async def test_tiles_endpoint_gives_us_registered_tiles(cms_requester):
    async with cms_requester as requester:
        # now test it...
        response, status = await requester('GET', '/db/guillotina/@tiles')
        assert status == 200
        assert len(response) >= 1
        assert '@tiles/' in response[0]['@id']

        response, status = await requester('GET', '/db/guillotina/@tiles/title')
        assert status == 200
        assert response["type"] == "object"


def test_conversation_behavior_returns_instance(dummy_request):
    ob = create_content(Resource)
    behavior = ITiles(ob)
    assert isinstance(behavior, Tiles)


async def test_storing_tiles_behavior_data(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'POST',
            '/db/guillotina/',
            data=json.dumps({
                '@type': 'Folder',
                'title': 'foobar',
                'id': 'foobar',
                '@behaviors': ['guillotina_cms.interfaces.tiles.ITiles'],
                'guillotina_cms.interfaces.tiles.ITiles': {
                    'tiles_layout': {
                        'cols': ['#title-1', '#description-1']
                    },
                    'tiles': {
                        '#title-1': {
                            "@type": "title"
                        }
                    }
                }
            })
        )
        assert status == 201

        resp, status = await requester(
            'GET',
            '/db/guillotina/foobar'
        )
        assert status == 200
        assert 'guillotina_cms.interfaces.tiles.ITiles' in resp
        assert 'tiles_layout' in resp['guillotina_cms.interfaces.tiles.ITiles']
