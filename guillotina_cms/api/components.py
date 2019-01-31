from guillotina import configure
from guillotina.api.service import Service
from guillotina.component import query_utility
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import ICatalogUtility
from guillotina.interfaces import IDatabase
from guillotina.interfaces import IResource
from guillotina.utils import get_content_depth
from guillotina.utils import get_content_path

from guillotina_cms.interfaces import ICMSLayer
from guillotina_cms.search.parser import SEARCH_DATA_FIELDS


@configure.service(
    context=IResource, method='GET',
    layer=ICMSLayer,
    permission='guillotina.AccessContent', name='@breadcrumbs',
    summary='Components for a bredcrumbs',
    responses={
        "200": {
            "description": "Result results on breadcrumbs",
            "schema": {
                "type": "object",
                "properties": {
                    "@id": "string",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "@id": {"type": "string"},
                                "title": {"type": "string"},
                            }
                        }
                    }
                }
            }
        }
    })
class Breadcrumbs(Service):

    async def __call__(self):
        result = []
        context = self.context
        while context is not None and not IDatabase.providedBy(context):
            result.append({
                'title': context.title,
                '@id': IAbsoluteURL(context, self.request)()
            })
            context = getattr(context, '__parent__', None)
        result.reverse()

        return {
            "@id": self.request.url.human_repr(),
            "items": result
        }


def recursive_fill(mother_list, pending_dict):
    for element in mother_list:
        if element['@id'] in pending_dict:
            element['items'] = pending_dict[element['@id']]
            recursive_fill(element['items'], pending_dict)


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@navigation',
    summary='Navigation view',
    responses={
        "200": {
            "description": "Result results on navigation",
            "schema": {
                "type": "object",
                "properties": {
                    "@id": "string",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "@id": {"type": "string"},
                                "title": {"type": "string"},
                            }
                        }
                    }
                }
            }
        }
    })
class Navigation(Service):

    async def __call__(self):
        search = query_utility(ICatalogUtility)
        context = self.request.container
        path = get_content_path(context)
        depth = get_content_depth(context) + 1
        max_depth = None
        if 'expand.navigation.depth' in self.request.rel_url.query:
            max_depth = str(int(self.request.rel_url.query['expand.navigation.depth']) + depth)
            musts = [
                {'range': {'depth': {'gte': depth}}},
                {'range': {'depth': {'lte': max_depth}}}]
        else:
            musts = [{'term': {'depth': depth}}]
        query = {
            'stored_fields': SEARCH_DATA_FIELDS,
            'query': {
                'bool': {
                    'must': musts,
                }
            },
            'sort': [{'position_in_parent': 'desc'}],
        }
        call_params = {
            'container': self.request.container,
            'path': path,
            'query': query,
            'size': 100
        }
        result = await search.get_by_path(**call_params)

        pending_dict = {}
        for brain in result['member']:
            brain_serialization = {
                'title': brain['title'],
                '@id': brain['@absolute_url']
            }
            pending_dict.setdefault(brain['parent_uuid'], []).append(brain_serialization)

        parent_uuid = context.uuid
        if parent_uuid not in pending_dict:
            final_list = []
        else:
            final_list = pending_dict[parent_uuid]
        if max_depth is not None:
            recursive_fill(final_list, pending_dict)

        return {
            "@id": self.request.url.human_repr(),
            "items": final_list
        }


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@actions',
    summary='Actions view',
    responses={
        "200": {
            "description": "Result results on actions",
            "schema": {
                "properties": {}
            }
        }
    })
class Actions(Service):

    async def __call__(self):
        return {
            'document_actions': [],
            'object': [
                {
                    'icon': '',
                    'id': 'view',
                    'title': 'View'
                },
                {
                    'icon': '',
                    'id': 'edit',
                    'title': 'Edit'
                },
                {
                    'icon': '',
                    'id': 'add',
                    'title': 'Add'
                },
                {
                    'icon': '',
                    'id': 'folderContents',
                    'title': 'Contents'
                },
                {
                    'icon': '',
                    'id': 'history',
                    'title': 'History'
                },
                {
                    'icon': '',
                    'id': 'local_roles',
                    'title': 'Sharing'
                }
            ],
            'object_buttons': [
                {
                    'icon': '',
                    'id': 'rename',
                    'title': 'Rename'
                }
            ],
            'portal_tabs': [
                {
                    'icon': '',
                    'id': 'index_html',
                    'title': 'Home'
                }
            ],
            'site_actions': [],
            'user': [
                {
                    'icon': '',
                    'id': 'preferences',
                    'title': 'Preferences'
                },
                {
                    'icon': '',
                    'id': 'plone_setup',
                    'title': 'Site Setup'
                },
                {
                    'icon': '',
                    'id': 'logout',
                    'title': 'Log out'
                }
            ]
        }
