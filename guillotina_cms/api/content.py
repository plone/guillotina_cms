from guillotina import configure
from guillotina.api.content import resolve_uid
from guillotina.interfaces import IContainer


@configure.service(
    method='GET', name="resolveuid/{uid}", context=IContainer,
    permission='guillotina.AccessContent',
    summary='Get content by UID',
    responses={
        "200": {
            "description": "Successful"
        }
    })
async def plone_resolve_uid(context, request):
    '''
    b/w compatible plone endpoint name
    '''
    return await resolve_uid(context, request)
