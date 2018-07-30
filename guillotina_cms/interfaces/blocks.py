from zope.interface import Interface
from guillotina.schema import JSONField
import json

LAYOUT_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'cols': {'type': 'array'}
    },
})

DATA_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'blocks': {'type': 'array'}
    },
})


class IBlocksMarker(Interface):
    """Marker interface for content with blocks."""


class IBlocks(Interface):
    layout = JSONField(
        title='Layout of the block',
        schema=LAYOUT_SCHEMA)

    blocks = JSONField(
        title='Data of the block',
        schema=DATA_SCHEMA)
