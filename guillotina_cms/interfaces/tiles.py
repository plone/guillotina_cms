from guillotina import schema
from guillotina.schema import JSONField
from zope.interface import Interface

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


class ITiles(Interface):
    tiles_layout = JSONField(
        title='Layout of the block',
        schema=LAYOUT_SCHEMA)

    tiles = JSONField(
        title='Data of the block',
        schema=DATA_SCHEMA)


class ITileType(Interface):
    """A utility that describes a type of tile
    """
    __name__ = schema.DottedName(
        title='Tile name (same as utility name)'
    )
    title = schema.TextLine(title=u'Title')
    description = schema.Text(title=u'Description', required=False)
    icon = schema.Text(title=u'Icon', required=False)
    add_permission = schema.Id(title=u'Zope 3 IPermission utility name')
    schema = schema.Object(
        title=u'Tile schema',
        description='Describes configurable data for this tile and allows a '
                    'form to be rendered to edit it. Set to None if the tile '
                    'has no configurable schema',
        schema=Interface,
        required=False,
    )
