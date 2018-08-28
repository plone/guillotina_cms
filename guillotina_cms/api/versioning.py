# -*- encoding: utf-8 -*-
from guillotina.configure import service
from guillotina.behaviors.dublincore import IDublinCore
from guillotina_cms.interfaces import IVersioning
from guillotina.interfaces import IResource

import logging


logger = logging.getLogger('guillotina_versioning')


@service(context=IResource, name='@versions', method='GET',
         permission='guillotina.ViewContent',
         parameters=[{
             "name": "size",
             "in": "query",
             "type": "number",
             "default": 20
         }, {
             "name": "cursor",
             "in": "query",
             "type": "string",
             "default": None
         }],
         responses={
             "200": {
                 "description": "Successful"
             }
         })
async def get_versions(context, request):
    cursor = request.GET.get('cursor')

    try:
        size = int(request.GET['size'])
    except KeyError:
        size = 20

    if cursor is None:
        dublincore = IDublinCore(context)
        await dublincore.load()
        items = [{
            'timestamp': dublincore.creation_date,
            'diff': None,
            'id': 'current',
            'stub': True,
            'filename': None,
            'size': None,
            'content_type': None
        }]
    else:
        items = []

    versioning = IVersioning(context, None)
    if versioning is None:
        return {
            'items': items,
            'total': len(items),
            'cursor': None
        }
    await versioning.load()
    if versioning.diffs is None:
        return {
            'items': items,
            'total': len(items),
            'cursor': None
        }
    diffs = versioning.diffs
    current_annotation_index = diffs.current_annotation_index
    metadata = diffs.annotations_metadata.get(current_annotation_index, {})
    start = metadata.get('len', 0)
    if cursor and cursor != 'current':
        current_annotation_index, start = cursor.split('-')
        current_annotation_index = int(current_annotation_index)
        start = int(start)
    batch_size = size
    while current_annotation_index >= 0 and len(items) < size:
        annotation = await diffs.get_annotation(
            context, current_annotation_index, create=False)
        if annotation is not None:
            end = max(start - batch_size, 0)
            for idx, item in enumerate(reversed(annotation['items'][end:start])):
                item_idx = annotation['items'].index(item)
                items.append({
                    'timestamp': item.get('timestamp'),
                    'diff': item.get('diff'),
                    'filename': item.get('filename'),
                    'size': item.get('size'),
                    'content_type': item.get('content_type'),
                    'id': f'{current_annotation_index}-{item_idx}',
                    'stub': item.get('stub', False)
                })
                batch_size -= 1
            cursor = f'{current_annotation_index}-{end}'
        if current_annotation_index == 0:
            break
        current_annotation_index -= 1
        metadata = diffs.annotations_metadata.get(current_annotation_index, {})
        start = metadata.get('len', 0)
    return {
        'items': items,
        'total': len(diffs) + 1,
        'cursor': cursor
    }
