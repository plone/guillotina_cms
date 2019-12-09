from guillotina import configure
from guillotina.catalog.utils import parse_query
from guillotina.interfaces import IResource
from guillotina.utils import find_container
from guillotina_cms.utils import get_search_utility
import itertools
from collections import Counter


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
            '@id': request.url,
            'items': [],
            'items_total': 0
        }

    parsed_query = parse_query(context, query, search)
    container = find_container(context)
    result = await search.search(container, parsed_query)

    return {
        '@id': request.url,
        'items': result['member'],
        'items_total': result['items_count'],
        'batching': {
            'from': parsed_query['_from'] or 0,
            'size': parsed_query['size']
        }
    }



@configure.service(
    context=IResource, method='GET', permission='guillotina.AccessContent', name='@suggestion',
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
async def suggestion_get(context, request):
    query = request.query.copy()
    search = get_search_utility(query)
    if search is None:
        return {}

    fields = request.query.get('_metadata', '').split(',')
    result = await search.query_aggregation(context, query)
    if 'member' in result:
        aggregation = []
        for field in fields:
            aggregation.append([])

        for items in result['member']:
            for index, item in enumerate(items):
                if isinstance(item, list):
                    aggregation[index].extend(item)
                elif isinstance(item, str):
                    aggregation[index].append(item)

        final_result = {}

        for index, field in enumerate(fields):
            elements = dict(Counter(aggregation[index]))
            final_result[field] = {
                "items": elements,
                "total": len(elements)
            } 
        return final_result
    else: 
        return {}

