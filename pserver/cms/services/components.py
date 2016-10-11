from zope.component import adapter
from zope.interface import implementer
from plone.server.interfaces import IObjectComponent
from plone.server.interfaces import IRequest
from plone.server.interfaces import IAbsoluteURL
from plone.dexterity.interfaces import IDexterityContent
from plone.server.interfaces import IPloneSite


@implementer(IObjectComponent)
@adapter(IDexterityContent, IRequest)
class Component(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request


class ComponentsGET(TraversableService):

    def publishTraverse(self, traverse):
        if len(traverse) == 1:
            # we want have the key of the registry
            self.value = queryMultiAdapter(
                (self.context, self.request),
                IObjectComponent, name=traverse[0])
            self.component_id = traverse[0]
        else:
            self.value = None
            self.component_id = None
        return self

    async def __call__(self):
        component = {
            'id': self.component_id,
            'data': {
                'items': self.value()
            }
        }
        return component


class Breadcrumbs(Component):

    def __call__(self):
        result = []
        context = self.context
        while context:
            result.append({
                'title': context.__name__,
                'url': IAbsoluteURL(context, self.request)(site_url=True)
            })
            context = getattr(context, '__parent__', None)
            if IPloneSite.providedBy(context):
                context = None
        result.reverse()
        return result


class Navigation(Component):

    def __call__(self):
        result = []
        site = self.request.site
        for content in site.values():
            if IDexterityContent.providedBy(content):
                result.append({
                    'title': content.__name__,
                    'url': IAbsoluteURL(content, self.request)(site_url=True)
                })
        return result