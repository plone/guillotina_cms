from guillotina import error_reasons
from guillotina.content import get_cached_factory
from guillotina.response import ErrorResponse
from guillotina import configure
from guillotina.interfaces import IResource


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.ManageConstraints', name='@constraints',
    summary='Get Type Constraints on a Resource')
async def get_constraints(context, request):
    at = getattr(context, '__allowed_types__', None)
    if at is None:
        tn = getattr(context, 'type_name', None)
        factory = get_cached_factory(tn)
        at = factory.allowed_types if factory.allowed_types is not None else []
    return at

@configure.service(
    context=IResource, method='POST',
    permission='guillotina.ManageConstraints', name='@constraints',
    summary='Set Type Constraints on a Resource',
    parameters=[{
        "name": "body",
        "in": "body",
        "type": "list"
    }],)
async def set_constraint(context, request):
    # validate input
    data = await request.json()
    if not isinstance(data, list):
        raise ErrorResponse(
            'MissingList', str('value type'),
            status=412, reason=error_reasons.DESERIALIZATION_FAILED)

    tn = getattr(context, 'type_name', None)
    factory = get_cached_factory(tn)
    allowed_types = factory.allowed_types
    for element in data:
        if allowed_types is not None and element not in allowed_types:
            raise ErrorResponse(
                'WrongType', str('wrong type'),
                status=412, reason=error_reasons.DESERIALIZATION_FAILED)

    setattr(context, '__allowed_types__', data)
    context._p_register()


@configure.service(
    context=IResource, method='PATCH',
    permission='guillotina.ManageConstraints', name='@constraints',
    summary='Patch Type Constraints on a Resource',
    parameters=[{
        "name": "body",
        "in": "body",
        "schema": {
            "properties": {
                "op": {
                    "type": "string"},  # add / del
                "types": {
                    "type": "array"}
            }
        }
    }],)
async def append_constraint(context, request):
    data = await request.json()
    if not isinstance(data, dict):
        raise ErrorResponse(
            'MissingLDict', str('value type'),
            status=412, reason=error_reasons.DESERIALIZATION_FAILED)

    operation = data['op']
    patch_data = data['types']
    if operation == 'add':
        tn = getattr(context, 'type_name', None)
        factory = get_cached_factory(tn)
        allowed_types = factory.allowed_types
        for element in patch_data:
            if allowed_types is not None and element not in allowed_types:
                raise ErrorResponse(
                    'WrongType', str('wrong type'),
                    status=412, reason=error_reasons.DESERIALIZATION_FAILED)

        at = getattr(context, '__allowed_types__', None)
        if at is None and allowed_types is not None:
            at = allowed_types.copy()
        elif at is None:
            at = []
        for element in patch_data:
            if element not in at:
                at.append(element)
        setattr(context, '__allowed_types__', at)
    elif operation == 'del':
        at = getattr(context, '__allowed_types__', None)
        if at is None:
            factory = get_cached_factory(tn)
            if factory.allowed_types is None:
                at = []
            else:
                at = factory.allowed_types.copy()
        for element in patch_data:
            if element in at:
                at.remove(element)
        setattr(context, '__allowed_types__', at)
    context._p_register()
