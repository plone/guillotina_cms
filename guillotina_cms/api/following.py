from guillotina import configure
from guillotina.event import notify
from guillotina.events import ObjectModifiedEvent
from guillotina_cms.interfaces import IFollowingMarker
from guillotina_cms.interfaces import IFollowing
from guillotina.utils import get_authenticated_user_id
from guillotina_cms.interfaces import ICMSLayer


@configure.service(
    context=IFollowingMarker, layer=ICMSLayer, name='@favorite',
    method='POST', permission='guillotina.AccessContent')
async def addfavorite(context, request):
    user = get_authenticated_user_id(request)
    behavior = IFollowing(context)
    await behavior.load(True)
    users_list = behavior.favorites
    if not users_list:
        behavior.favorites = []
        users_list = behavior.favorites
    if user not in users_list:
        users_list.append(user)
    behavior.data._p_register()
    await notify(ObjectModifiedEvent(context, payload={
        'favorites': ''
    }))


@configure.service(
    context=IFollowingMarker, name='@favorite', method='DELETE',
    permission='guillotina.AccessContent')
async def deletefavorite(context, request):
    user = get_authenticated_user_id(request)
    behavior = IFollowing(context)
    await behavior.load(True)
    users_list = behavior.favorites
    if users_list is None:
        behavior.favorites = []
        users_list = behavior.favorites
    if user in users_list:
        users_list.remove(user)
    behavior.data._p_register()
    await notify(ObjectModifiedEvent(context, payload={
        'favorites': ''
    }))
