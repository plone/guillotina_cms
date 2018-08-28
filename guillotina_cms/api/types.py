# -*- coding: utf-8 -*-
from guillotina import configure
from guillotina.api.service import Service
from guillotina.component import getMultiAdapter
from guillotina.component import queryUtility
from guillotina.interfaces import IResource
from guillotina.interfaces import IFactorySerializeToJson
from guillotina.interfaces import IResourceFactory
from guillotina.interfaces import IAbsoluteURL
from guillotina.response import HTTPNotFound
from guillotina.interfaces import IConstrainTypes
from guillotina._cache import FACTORY_CACHE
from guillotina._cache import PERMISSIONS_CACHE
from guillotina.interfaces import IPermission
from guillotina.component import query_utility
from guillotina.interfaces import IInteraction
from guillotina.exceptions import NoPermissionToAdd
from guillotina.interfaces import IContainer


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@types',
    summary='Read information on available types',
    responses={
        "200": {
            "description": "Result results on types",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "@id": {"type": "string"},
                        "title": {"type": "string"},
                        "addable": {"type": "boolean"}
                    }
                }
            }
        }
    })
@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@types',
    summary='Read information on available types',
    responses={
        "200": {
            "description": "Result results on types",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "@id": {"type": "string"},
                        "title": {"type": "string"},
                        "addable": {"type": "boolean"}
                    }
                }
            }
        }
    })
async def get_all_types(context, request):
    result = []
    base_url = IAbsoluteURL(context, request)()
    constrains = IConstrainTypes(context, None)

    for id, factory in FACTORY_CACHE.items():
        add = True
        if constrains is not None:
            if not constrains.is_type_allowed(id):
                add = False

        if factory.add_permission:
            if factory.add_permission in PERMISSIONS_CACHE:
                permission = PERMISSIONS_CACHE[factory.add_permission]
            else:
                permission = query_utility(
                    IPermission, name=factory.add_permission)
                PERMISSIONS_CACHE[factory.add_permission] = permission

            if permission is not None and \
                    not IInteraction(request).check_permission(
                        permission.id, context):
                add = False
        if add:
            result.append({
                '@id': base_url + '/@types/' + id,
                'addable': True,
                'title': id
            })
    return result


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@types/{type_id}',
    summary='Components for a resource',
    responses={
        "200": {
            "description": "Result results on types",
            "schema": {
                "properties": {}
            }
        }
    })
@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@types/{type_id}',
    summary='Components for a resource',
    responses={
        "200": {
            "description": "Result results on types",
            "schema": {
                "properties": {}
            }
        }
    })
class Read(Service):

    async def prepare(self):
        type_id = self.request.matchdict['type_id']
        self.value = queryUtility(IResourceFactory, name=type_id)
        if self.value is None:
            raise HTTPNotFound(content={
                'reason': f'Could not find type {type_id}',
                'type': type_id
            })

    async def __call__(self):
        serializer = getMultiAdapter(
            (self.value, self.request),
            IFactorySerializeToJson)

        result = await serializer()
        return result
