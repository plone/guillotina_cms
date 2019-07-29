from guillotina import configure
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IResource
from guillotina.component import getMultiAdapter
from guillotina.response import ErrorResponse
from guillotina.response import HTTPUnauthorized
from guillotina.response import Response
from guillotina.utils import get_authenticated_user_id
from guillotina.utils import get_security_policy
from guillotina_cms.interfaces import ICMSBehavior

from copy import deepcopy
import uuid
from datetime import datetime


@configure.service(
    method="GET",
    name="@comments",
    context=IResource,
    permission="guillotina.ViewComments",
    summary="Get comments on a resource",
    responses={"200": {"description": "Successful"}},
)
async def list_comments(context, request):
    bhr = ICMSBehavior(context)
    if not bhr.allow_discussion:
        raise HTTPUnauthorized(content={"text": "Not available option"})
    await bhr.load()
    url = getMultiAdapter((context, request), IAbsoluteURL)()
    result = []
    response = {"@id": url + "/@comments", "items": result}

    if bhr.comments is None:
        return response
    for key, value in bhr.comments.items():
        new_comment = deepcopy(value)
        new_comment["@type"] = "Discussion Item"
        if new_comment.get("@parent", False):
            new_comment["@parent"] = url + new_comment.get("@parent")
        new_comment["@id"] = url + "/@comments/" + key
        new_comment["comment_id"] = key
        result.append(new_comment)

    return response


@configure.service(
    method="POST",
    name="@comments",
    context=IResource,
    permission="guillotina.AddComments",
    summary="Add comment on a resource",
    responses={"200": {"description": "Successful"}},
)
async def add_comment(context, request):
    payload = await request.json()
    bhr = ICMSBehavior(context)
    if not bhr.allow_discussion:
        raise HTTPUnauthorized(content={"text": "Not available option"})
    await bhr.load()

    if bhr.comments is None:
        bhr.comments = {}

    user_id = get_authenticated_user_id()
    comment_uuid = uuid.uuid4().hex
    bhr.comments[comment_uuid] = {
        "@parent": None,
        "author_name": None,
        "author_username": user_id,
        "creation_date": datetime.now().isoformat(),
        "in_reply_to": None,
        "is_deletable": True,
        "is_editable": True,
        "modification_date": datetime.now().isoformat(),
        "text": {"data": payload.get("text", ""), "mime-type": "text/plain"},
        "user_notification": None,
    }

    bhr.register()

    url = getMultiAdapter((context, request), IAbsoluteURL)()
    headers = {"Location": url + "/@comments/" + comment_uuid}
    return Response(status=204, headers=headers)


@configure.service(
    method="POST",
    name="@comments/{comment_id}",
    context=IResource,
    permission="guillotina.AddComments",
    summary="Add comment on a resource",
    responses={"200": {"description": "Successful"}},
)
async def add_child_comment(context, request):
    payload = await request.json()
    comment_id = request.matchdict["comment_id"]
    bhr = ICMSBehavior(context)
    if not bhr.allow_discussion:
        raise HTTPUnauthorized(content={"text": "Not available option"})
    await bhr.load()

    if comment_id not in bhr.comments:
        raise ErrorResponse("InvalidComment", "This comment does not exist", status=412)

    user_id = get_authenticated_user_id()
    new_comment_uuid = uuid.uuid4().hex
    bhr.comments[new_comment_uuid] = {
        "@parent": comment_id,
        "author_name": None,
        "author_username": user_id,
        "creation_date": datetime.now().isoformat(),
        "in_reply_to": None,
        "is_deletable": True,
        "is_editable": True,
        "modification_date": datetime.now().isoformat(),
        "text": {"data": payload.get("text", ""), "mime-type": "text/plain"},
        "user_notification": None,
    }

    bhr.register()

    url = getMultiAdapter((context, request), IAbsoluteURL)()
    headers = {"Location": url + "/@comments/" + new_comment_uuid}
    return Response(status=204, headers=headers)


@configure.service(
    method="PATCH",
    name="@comments/{comment_id}",
    context=IResource,
    permission="guillotina.ModifyComments",
    summary="Modify comment on a resource",
    responses={"200": {"description": "Successful"}},
)
async def modify_comment(context, request):
    payload = await request.json()
    comment_id = request.matchdict["comment_id"]
    bhr = ICMSBehavior(context)
    if not bhr.allow_discussion:
        raise HTTPUnauthorized(content={"text": "Not available option"})
    await bhr.load()

    if comment_id not in bhr.comments:
        raise ErrorResponse("InvalidComment", "This comment does not exist", status=412)

    user_id = get_authenticated_user_id()
    comment = bhr.comments[comment_id]

    # TODO: We need ?
    if user_id != comment["author_username"]:
        raise HTTPUnauthorized(content={"text": "Not the author"})

    comment["text"]["data"] = payload.get("text", "")
    comment["modification_date"] = datetime.now().isoformat()

    bhr.register()

    url = getMultiAdapter((context, request), IAbsoluteURL)()
    headers = {"Location": url + "/@comments/" + comment_id}
    return Response(status=204, headers=headers)


def delete_from_list(obj_dict, pending_list):
    build_list = [x for x in obj_dict.keys()]
    found = True
    while found:
        found = False
        new_list = build_list
        build_list = []
        for key in new_list:
            if obj_dict[key]["@parent"] in pending_list and key not in pending_list:
                found = True
                pending_list.append(key)
            else:
                build_list.append(key)


@configure.service(
    method="DELETE",
    name="@comments/{comment_id}",
    context=IResource,
    permission="guillotina.DeleteComments",
    summary="Delete comment on a resource",
    responses={"200": {"description": "Successful"}},
)
async def delete_comment(context, request):
    comment_id = request.matchdict["comment_id"]
    bhr = ICMSBehavior(context)
    if not bhr.allow_discussion:
        raise HTTPUnauthorized(content={"text": "Not available option"})
    await bhr.load()

    if comment_id not in bhr.comments:
        raise ErrorResponse("InvalidComment", "This comment does not exist", status=412)

    user_id = get_authenticated_user_id()
    comment = bhr.comments[comment_id]

    # TODO: We need ?
    policy = get_security_policy()
    if user_id != comment["author_username"] or not policy.check_permission(
        "guillotina.DeleteAllComments", context
    ):
        raise HTTPUnauthorized(content={"text": "Not the author or permission"})

    list_to_delete = [comment_id]
    delete_from_list(bhr.comments, list_to_delete)
    for comment in list_to_delete:
        del bhr.comments[comment]

    bhr.register()

    return Response(status=204)
