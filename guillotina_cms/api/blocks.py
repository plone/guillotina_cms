
from os.path import join

from guillotina import app_settings
from guillotina import configure
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IContainer
from guillotina.interfaces import ISchemaSerializeToJson
from guillotina.response import HTTPNotFound
from guillotina.utils import resolve_dotted_name
from guillotina.interfaces import ILayoutComponents


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@blocks',
    summary='Get available blocks')
async def get_blocks(context, request):
    result = []
    for key, item in app_settings['available_blocks'].items():
        result.append({
            "@id": join(IAbsoluteURL(context)(), "@blocks", item["name"]),
            "title": item['title'],
            "description": item['description']
        })
    return result


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@layout_components',
    summary='Get available layout components')
async def get_layout_components(context, request):
    registry = await get_registry()
    settings = registry.for_interface(ILayoutComponents)
    return settings['components']


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@blocks/{key}',
    summary='Get specific block')
async def get_block_schema(context, request):
    key = request.matchdict['key']
    if key not in app_settings['available_blocks'].keys():
        return HTTPNotFound()
    block = app_settings['available_blocks'][key]
    schema = resolve_dotted_name(block['schema'])
    serializer = get_multi_adapter((schema, request), ISchemaSerializeToJson)
    return await serializer()
