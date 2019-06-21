from guillotina import configure
from guillotina.catalog.utils import parse_query
from guillotina.interfaces import IResource
from guillotina.utils import find_container
from guillotina_cms.utils import get_search_utility


@configure.service(
    context=IResource, method='GET', permission='guillotina.AccessContent', name='@search',
    summary='Make search request',
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
    query = request.query.copy()
    search = get_search_utility(query)
    if search is None:
        return {
            '@id': request.url.human_repr(),
            'items': [],
            'items_total': 0
        }

    parsed_query = parse_query(context, query, search)
    container = find_container(context)
    result = await search.search(container, parsed_query)

    return {
        '@id': request.url.human_repr(),
        'items': result['member'],
        'items_total': result['items_count'],
        'batching': {
            'from': parsed_query['_from'] or 0,
            'size': parsed_query['size']
        }
    }
