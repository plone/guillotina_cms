from guillotina import configure
from guillotina.db.interfaces import IJSONDBSerializer
from guillotina.interfaces import IResource
from guillotina.utils import get_content_path
from guillotina.interfaces import IContainer


@configure.adapter(
    for_=IResource,
    provides=IJSONDBSerializer)
class JSONDBSerializer:

    def __init__(self, context):
        self.context = context

    async def __call__(self):
        container = self.context
        while not IContainer.providedBy(container) and container is not None:
            container = container.__parent__
        return {
            'position_in_parent': getattr(self.context, 'position_in_parent', -1),
            'parent_id': self.context.__parent__.id,
            'path': get_content_path(self.context),
            'container_id': getattr(container, 'id', None)
        }
