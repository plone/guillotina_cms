import base64
import json

from guillotina.utils import resolve_path
from guillotina_cms.behaviors.image import IImageAttachment


async def _add_image(requester, path):
    image_path = resolve_path(
        'guillotina:static/assets/apple-touch-icon-144x144.png')
    with open(image_path, 'rb') as fi:
        image_data = base64.b64encode(fi.read()).decode('utf-8')
    await requester(
        'PATCH', path,
        data=json.dumps({
            IImageAttachment.__identifier__: {
                'image': {
                    'filename': 'logo.png',
                    'content-type': 'image/png',
                    'encoding': 'base64',
                    'data': image_data
                }
            }
        })
    )


async def test_add_container_logo(cms_requester):
    async with cms_requester as requester:

        await _add_image(requester, '/db/guillotina')

        resp, status = await requester(
            'GET',
            '/db/guillotina/@download/image'
        )
        assert status == 200
        assert len(resp) > 0

        resp, status = await requester(
            'GET',
            '/db/guillotina/@@images/image'
        )
        assert status == 200
        assert len(resp) > 0


async def test_get_scales(cms_requester):
    async with cms_requester as requester:

        await _add_image(requester, '/db/guillotina')

        resp, status = await requester(
            'GET',
            '/db/guillotina/@@images/image/mini'
        )
        assert status == 200
        assert len(resp) > 0


async def test_fourohfour_when_no_image(cms_requester):
    async with cms_requester as requester:
        resp, status = await requester(
            'GET',
            '/db/guillotina/@@images/foobar'
        )
        assert status == 404


async def test_fourohfour_when_invalid_scale(cms_requester):
    async with cms_requester as requester:
        await _add_image(requester, '/db/guillotina')

        resp, status = await requester(
            'GET',
            '/db/guillotina/@@images/image/foobar'
        )
        assert status == 404


async def test_get_scales_on_image_content(cms_requester):
    async with cms_requester as requester:

        image_path = resolve_path(
            'guillotina:static/assets/apple-touch-icon-144x144.png')
        with open(image_path, 'rb') as fi:
            image_data = base64.b64encode(fi.read()).decode('utf-8')
        _, status = await requester(
            'POST', '/db/guillotina',
            data=json.dumps({
                'id': 'logo.png',
                '@type': 'Image',
                'image': {
                    'filename': 'logo.png',
                    'content-type': 'image/png',
                    'encoding': 'base64',
                    'data': image_data
                }
            })
        )
        assert status == 201

        resp, status = await requester(
            'GET',
            '/db/guillotina/logo.png'
        )
        assert status == 200

        resp, status = await requester(
            'GET',
            '/db/guillotina/logo.png/@@images/image/mini'
        )
        assert status == 200
        assert len(resp) > 0

