from guillotina import configure
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IResource
from guillotina.interfaces import IContainer
from guillotina.interfaces import IDatabase
from guillotina.api.service import Service
from guillotina_cms.interfaces import ICMSLayer


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
        result = []
        container = self.request.container
        async for content in container.async_values():
            if IResource.providedBy(content):
                result.append({
                    'title': content.title,
                    '@id': IAbsoluteURL(content, self.request)()
                })
        return {
            "@id": self.request.url.human_repr(),
            "items": result
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
