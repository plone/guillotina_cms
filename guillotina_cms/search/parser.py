# https://docs.google.com/document/d/1xooubzJKBnUzVlsa2f0GSwvuE1oir9hUdWUf1SU9S6E/edit
from guillotina.utils import get_content_path
from guillotina.directives import index
from guillotina.directives import metadata
from guillotina.directives import merged_tagged_value_dict
from guillotina.directives import merged_tagged_value_list
from guillotina.component import get_utilities_for
from guillotina.interfaces import IBehavior
from guillotina._cache import FACTORY_CACHE
from guillotina.utils import get_content_depth
from dateutil.parser import parse
import logging


logger = logging.getLogger('guillotina_cms')

INDEXES_CACHE = None
MAX_AGGS = 20


def convert(value):
    # XXX: Check for possible json injection
    return value.split(' ')


def get_indexes():
    """ Get all the indexes
    """

    global INDEXES_CACHE
    if INDEXES_CACHE is None:
        mapping = {}
        for type_name, type_schema in FACTORY_CACHE.items():
            mapping.update(merged_tagged_value_dict(type_schema.schema, index.key))
        for _, utility in get_utilities_for(IBehavior):
            mapping.update(merged_tagged_value_dict(utility.interface, index.key))
        INDEXES_CACHE = mapping
    else:
        INDEXES_CACHE
    return INDEXES_CACHE


def get_metadata():
    global METADATA_CACHE
    if METADATA_CACHE is None:
        mapping = []
        for type_name, type_schema in FACTORY_CACHE.items():
            mapping.extend(merged_tagged_value_list(type_schema.schema, metadata.key))
        for _, utility in get_utilities_for(IBehavior):
            mapping.extend(merged_tagged_value_list(utility.interface, metadata.key))
        METADATA_CACHE = mapping
    else:
        METADATA_CACHE
    return METADATA_CACHE


def process_field(field, value, query):

    indices = get_indexes()
    modifier = None
    if field == 'portal_type':
        # XXX: Compatibility with plone?
        field = 'type_name'

    if field not in indices:
        if field.endswith('__not'):
            modifier = 'not'
            field = field.rstrip('__not')
        elif field.endswith('__in'):
            modifier = 'in'
            field = field.rstrip('__in')
        elif field.endswith('__eq'):
            modifier = 'eq'
            field = field.rstrip('__eq')
        elif field.endswith('__gte'):
            modifier = 'gte'
            field = field.rstrip('__gte')
        elif field.endswith('__lte'):
            modifier = 'lte'
            field = field.rstrip('__lte')
        elif field.endswith('__wildcard'):
            modifier = 'wildcard'
            field = field.rstrip('__wildcard')

    if field == 'portal_type':
        # XXX: Compatibility with plone?
        field = 'type_name'

    if field in indices:
        if len(value) > 1:
            term_keyword = 'terms'
        else:
            term_keyword = 'term'
            value = value[0]

        _type = indices[field]['type']
        if _type == 'int':
            try:
                value = int(value)
            except ValueError:
                pass
        elif _type == 'date':
            value = parse(value).timestamp()

        elif _type == 'boolean':
            if value in ('true', 'True', 'yes'):
                value = True
            else:
                value = False

        if modifier is None:
            # Keyword we expect an exact match
            query['query']['bool']['must'].append(
                {
                    term_keyword: {
                        field: value
                    }
                })
        elif modifier == 'not':
            # Must not be
            query['query']['bool']['must_not'].append(
                {
                    term_keyword: {
                        field: value
                    }
                })
        elif modifier == 'in' and _type == 'text':
            # The value list can be inside the field
            query['query']['bool']['must'].append(
                {
                    'match': {
                        field: value
                    }
                })
        elif modifier == 'eq':
            # The sentence must appear as is it
            value = ' '.join(value)
            query['query']['bool']['must'].append(
                {
                    'match': {
                        field: value
                    }
                })
        elif modifier == 'gte':
            query['query']['bool']['must'].append(
                {
                    'range': {field: {'gte': value}}})
        elif modifier == 'lte':
            query['query']['bool']['must'].append(
                {
                    'range': {field: {'lte': value}}})
        elif modifier == 'wildcard':
            query['query']['bool']['must'].append(
                {
                    'wildcard': {
                        field: value
                    }
                })
        else:
            logger.warn(
                'wrong search type: %s modifier: %s field: %s value: %s' %
                (_type, modifier, field, value))


def bbb_parser(get_params):

    if 'path.depth' in get_params and 'sort_on' in get_params and 'b_size' in get_params:
        if 'SearchableText' in get_params:
            get_params['title_in'] = get_params['SearchableText']
            get_params['text_in'] = get_params['SearchableText']
            del get_params['SearchableText']

        if 'b_start' in get_params:
            get_params['_from'] = get_params['b_start']
            del get_params['b_start']

        if get_params['sort_on'] == 'getObjPositionInParent':
            get_params['_sort_des'] = 'position_in_parent'
            del get_params['sort_on']

        get_params['depth'] = get_params['path.depth']
        del get_params['path.depth']
        get_params['_size'] = get_params['b_size']
        del get_params['b_size']


class Parser:

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def __call__(self):
        get_params = dict(self.request.rel_url.query)

        # Fullobject
        if '_fullobject' in get_params:
            full_objects = True
            del get_params['_fullobject']
        else:
            full_objects = False

        query = {
            '_source': {
                'includes': [],
                'excludes': []
            },
            'query': {
                'bool': {
                    'must': [],
                    'must_not': []
                }
            },
            'sort': []
        }

        bbb_parser(get_params)

        if 'depth' in get_params:
            get_params['depth'] = str(int(get_params['depth']) + get_content_depth(self.context))

        if '_aggregations' in get_params:
            query['aggregations'] = {}
            for agg in convert(get_params['_aggregations']):
                if agg == 'portal_type':
                    # XXX: Compatibility with plone?
                    agg = 'type_name'
                query['aggregations'][agg] = {
                    'terms': {
                        'field': agg,
                        'size': MAX_AGGS}
                }
            del get_params['_aggregations']
        # Metadata
        if '_metadata' in get_params:
            query['_sources']['includes'] = convert(get_params['_metadata'])
            del get_params['_metadata']

        if '_metadata_not' in get_params:
            query['_sources']['excludes'] = convert(get_params['_metadata_not'])
            del get_params['_metadata_not']

        # From
        if '_from' in get_params:
            query['from'] = get_params['_from']
            del get_params['_from']

        # Sort
        if '_sort_asc' in get_params:
            for field in convert(get_params['_sort_asc']):
                query['sort'].append({field: 'asc'})
            del get_params['_sort_asc']

        if '_sort_des' in get_params:
            for field in convert(get_params['_sort_des']):
                query['sort'].append({field: 'desc'})
            del get_params['_sort_des']

        query['sort'].append({'_id': 'desc'})

        # Path specific use case
        if 'path__starts' in get_params:
            path = get_params['path__starts']
            path = '/' + '/'.join(convert(path))
            del get_params['path__starts']
        else:
            path = get_content_path(self.context)

        # TODO _aggregations

        call_params = {
            'container': self.request.container,
            'path': path,
            'query': query
        }

        if '_size' in get_params:
            call_params['size'] = get_params['_size']
            del get_params['_size']

        for field, value in get_params.items():
            process_field(field, convert(value), query)

        return call_params, full_objects
