from guillotina import configure
from guillotina import app_settings
from guillotina.interfaces import IResource
from guillotina.component import query_utility
from guillotina.interfaces import ICatalogUtility

from guillotina.utils import resolve_dotted_name
from guillotina.utils import get_object_by_oid
from guillotina.api.content import DefaultGET


@configure.service(
    context=IResource, method='GET', permission='guillotina.AccessContent', name='@search',
    summary='Make search request',
    parameters=[{
        "name": "q",
        "in": "query",
        "required": True,
        "type": "string"
    }],
    responses={
        "200": {
            "description": "Search results",
            "type": "object",
            "schema": {
                "$ref": "#/definitions/SearchResults"
            }
        }
    })
async def search_get(context, request):
    search = query_utility(ICatalogUtility)
    if search is None:
        return {
            '@id': request.url.human_repr(),
            'items': [],
            'items_total': 0
        }

    parser = resolve_dotted_name(app_settings['search_parser'])
    call_params, full_objects = parser(request, context)()

    result = await search.get_by_path(**call_params)

    real_result = {
        '@id': request.url.human_repr(),
        'items': [],
        'items_total': result['items_count']
    }

    for member in result['member']:
        if full_objects:
            obj = get_object_by_oid(member['uuid'])

            view = DefaultGET(obj, request)
            serialization = await view()
            real_result['items'].append(serialization)
        else:
            member['@id'] = member['@absolute_url']
            del member['@absolute_url']
    real_result['aggregations'] = {
        key: value['buckets'] for key, value in result.get('aggregations', {}).items()
    }
    real_result['items'] = result['member']
    return real_result
