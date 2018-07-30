
from os.path import join

from guillotina import app_settings
from guillotina import configure
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IContainer
from guillotina.interfaces import ISchemaSerializeToJson
from guillotina.response import HTTPNotFound
from guillotina.utils import resolve_dotted_name


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@tiles',
    summary='Get available tiles')
async def get_tiles(context, request):
    result = []
    for key, item in app_settings['available_tiles'].items():
        result.append({
            "@id":  join(IAbsoluteURL(context)(), "@tiles", item["name"]),
            "title": item['title'],
            "description": item['description']
        })
    return result


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@tiles/{key}',
    summary='Get specific tile')
async def get_tile_schema(context, request):
    key = request.matchdict['key']
    if key not in app_settings['available_tiles'].keys():
        return HTTPNotFound()
    tile = app_settings['available_tiles'][key]
    schema = resolve_dotted_name(tile['schema'])
    serializer = get_multi_adapter((schema, request), ISchemaSerializeToJson)
    return await serializer()
