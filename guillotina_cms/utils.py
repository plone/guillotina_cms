from guillotina import app_settings
from guillotina.catalog.utils import get_index_definition
from guillotina.interfaces import ICatalogUtility
from guillotina.component import query_utility

GUILLOTINA_LOGO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABxklEQVRYhe3WsW4TQRDG8d8c14AiI1EhypRAE4ooSoGi6JwoDxApT0DDC1Cm41WQKCkg9ilKgRCiAERBQWFRUFHgKEIUxNxSxILIdpwLdnDjqfZmb+b7797c7kQqJDO0bJbicwDIBx1RissUHKy5me/AHGAOMPQXXIalLQ09a2gOnruXApAeyHWsCE0Uji2fpTU1gLTltp5C0tSxhoU6t8w/A6RNN1V9wVA4dqt2cKjwXtKqDZA2XJOsCU1J4Ze7fydriX4WSsmezH7s+caYHUjbMl3Lsv4qK6vIa1/e4VCyL+zJlfFcZ+RrQ/1A5qFKE+to1JQj/JS8EtquaFnxNnZV54ZN1JCED/S39aqX8cyPuqFp0w3J+sWKMHzpC7Zlymj5ekFkqekxCpV7kmw8QDiSHKAt14oXPl1UcJjAo9OPgwA9vBbaQmnVm9jVm1h0jOX4KJRC23UH8dT3P7Ot8xOkQkNmB1SeROlonH/QJup+UqGBd1jsuzpY6o+H/FE6mm5HdLLCxVOeRZmdM/0jU8zYIm1b0HVfpinZiLY7dYOn8QlyXV3k559ZI+hPEi6dUYQj/UM5Bon+d1s+2VE8BZt5Ec4BfgMMY6BXJQhbPgAAAABJRU5ErkJggg=="


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

def get_default_logo():
    if 'default_logo' in app_settings:
        return app_settings['default_logo']
    else:
        return GUILLOTINA_LOGO