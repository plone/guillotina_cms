from guillotina import configure
from guillotina.api.service import Service
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IContainer
from guillotina.interfaces import IResource
from guillotina.utils import find_container
from guillotina.utils import get_content_depth
from guillotina_cms.interfaces import ICMSLayer
from guillotina_cms.utils import get_search_utility


@configure.service(
    context=IResource,
    method="GET",
    layer=ICMSLayer,
    permission="guillotina.AccessContent",
    name="@breadcrumbs",
    summary="Components for a bredcrumbs",
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
                            "properties": {"@id": {"type": "string"}, "title": {"type": "string"}},
                        },
                    },
                },
            },
        }
    },
)
class Breadcrumbs(Service):
    async def __call__(self):
        result = []
        context = self.context
        while context is not None and not IContainer.providedBy(context):
            result.append({"title": context.title, "@id": IAbsoluteURL(context, self.request)()})
            context = getattr(context, "__parent__", None)
        result.reverse()

        return {"@id": self.request.url, "items": result}


def recursive_fill(mother_list, pending_dict):
    for element in mother_list:
        if element["@name"] in pending_dict:
            element["items"] = pending_dict[element["@name"]]
            recursive_fill(element["items"], pending_dict)


@configure.service(
    context=IResource,
    method="GET",
    permission="guillotina.AccessContent",
    name="@navigation",
    summary="Navigation view",
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
                            "properties": {"@id": {"type": "string"}, "title": {"type": "string"}},
                        },
                    },
                },
            },
        }
    },
)
class Navigation(Service):
    async def __call__(self):
        search = get_search_utility()
        container = find_container(self.context)
        depth = get_content_depth(container)
        max_depth = None
        if "expand.navigation.depth" in self.request.query:
            max_depth = str(int(self.request.query["expand.navigation.depth"]) + depth)
            depth_query = {"depth__gte": depth, "depth__lte": max_depth}
        else:
            depth_query = {"depth": depth}

        depth_query["hidden_navigation"] = False
        result = await search.query(
            container, {**{"_sort_asc": "position_in_parent", "_size": 100}, **depth_query}
        )

        pending_dict = {}
        for brain in result["member"]:
            brain_serialization = {
                "title": brain.get("title"),
                "@id": brain.get("@id"),
                "@name": brain.get("uuid"),
                "description": ""
            }
            pending_dict.setdefault(brain.get("parent_uuid"), []).append(brain_serialization)

        parent_uuid = container.uuid
        if parent_uuid not in pending_dict:
            final_list = []
        else:
            final_list = pending_dict[parent_uuid]
        if max_depth is not None:
            recursive_fill(final_list, pending_dict)

        return {"@id": self.request.url, "items": final_list}


@configure.service(
    context=IResource,
    method="GET",
    permission="guillotina.AccessContent",
    name="@actions",
    summary="Actions view",
    responses={"200": {"description": "Result results on actions", "schema": {"properties": {}}}},
)
class Actions(Service):
    async def __call__(self):
        return {
            "document_actions": [],
            "object": [
                {"icon": "", "id": "view", "title": "View"},
                {"icon": "", "id": "edit", "title": "Edit"},
                {"icon": "", "id": "add", "title": "Add"},
                {"icon": "", "id": "folderContents", "title": "Contents"},
                {"icon": "", "id": "history", "title": "History"},
                {"icon": "", "id": "local_roles", "title": "Sharing"},
            ],
            "object_buttons": [{"icon": "", "id": "rename", "title": "Rename"}],
            "portal_tabs": [{"icon": "", "id": "index_html", "title": "Home"}],
            "site_actions": [],
            "user": [
                {"icon": "", "id": "preferences", "title": "Preferences"},
                {"icon": "", "id": "plone_setup", "title": "Site Setup"},
                {"icon": "", "id": "logout", "title": "Log out"},
            ],
        }
