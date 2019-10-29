from guillotina import schema
from guillotina.schema import JSONField
from zope.interface import Interface
from guillotina.schema.interfaces import IContextAwareDefaultFactory
import json
from zope.interface import implementer


LAYOUT_SCHEMA = json.dumps({"type": "object", "properties": {"items": {"type": "array"}}})

DATA_SCHEMA = json.dumps({"type": "object", "properties": {}})


@implementer(IContextAwareDefaultFactory)
class ContextTilesLayoutFactory:
    def __call__(self, context):
        # Should be in a behavior
        if context is None:
            return None
        return IDefaultBlocksLayout(context.context)()


@implementer(IContextAwareDefaultFactory)
class ContextTilesFactory:
    def __call__(self, context):
        # Should be in a behavior
        if context is None:
            return None
        return IDefaultBlocks(context.context)()


class IDefaultBlocksLayout(Interface):
    pass


class IDefaultBlocks(Interface):
    pass


class ITiles(Interface):
    blocks_layout = JSONField(
        title="Layout of the block",
        required=False,
        defaultFactory=ContextTilesLayoutFactory(),
        schema=LAYOUT_SCHEMA,
        # missing_value={"items": []},
    )

    blocks = JSONField(
        title="Data of the block",
        required=False,
        defaultFactory=ContextTilesFactory(),
        # missing_value={},
        schema=DATA_SCHEMA,
    )


class ITileType(Interface):
    """A utility that describes a type of tile
    """

    __name__ = schema.DottedName(title="Tile name (same as utility name)")
    title = schema.TextLine(title=u"Title")
    description = schema.Text(title=u"Description", required=False)
    icon = schema.Text(title=u"Icon", required=False)
    add_permission = schema.Id(title=u"Zope 3 IPermission utility name")
    schema = schema.Object(
        title=u"Tile schema",
        description="Describes configurable data for this tile and allows a "
        "form to be rendered to edit it. Set to None if the tile "
        "has no configurable schema",
        schema=Interface,
        required=False,
    )
