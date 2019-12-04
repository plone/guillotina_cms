from guillotina import configure
from guillotina.utils import get_registry
from guillotina.interfaces import IContainer
from guillotina_cms.interfaces import IMenu


@configure.service(
    context=IContainer, method='GET', permission='guillotina.ViewContent',
    name='@menu')
async def menu(context, request):

    registry = await get_registry()
    settings = registry.for_interface(IMenu)
    return {
        'value': settings['definition']
    }

