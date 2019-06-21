from guillotina import app_settings
from guillotina.catalog.utils import get_index_definition
from guillotina.interfaces import ICatalogUtility
from guillotina.component import query_utility


def get_search_utility(query=None):
    query = query or {}
    if 'pg_catalog' not in app_settings['load_utilities']:
        return query_utility(ICatalogUtility)
    else:
        found = 'SearchableText' in query
        for key in query.keys():
            if key[0] == '_':
                continue
            index = get_index_definition(key)
            if index is None:
                continue
            if index['type'] in ('text', 'searchabletext'):
                found = True
                break

        if found:
            return query_utility(ICatalogUtility)
        return query_utility(ICatalogUtility, name='pg_catalog')
