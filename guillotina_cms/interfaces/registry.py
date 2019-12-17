from guillotina import schema
from guillotina_cms.utils import get_default_logo
from zope.interface import Interface
import json

MENU_LAYOUT = json.dumps({"type": "object", "properties": {}})

LAYOUT_TYPE_COMPONENTS = json.dumps(
    {
        "type": "object",
        "properties": {},
        "additionalProperties": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type" : "string"}
                }
            },
        },
    }
)


class IImagingSettings(Interface):
    allowed_sizes = schema.Dict(
        missing_value={
            "high": "1400:1400",
            "large": "768:768",
            "preview": "400:400",
            "mini": "200:200",
            "thumb": "128:128",
            "tile": "64:64",
            "icon": "32:32",
        }
    )

    quality = schema.Int(default=88)


class IMenu(Interface):

    definition = schema.JSONField(
        title="Menu definition", required=False, schema=MENU_LAYOUT, defaultFactory=list
    )

    logo = schema.Text(title="Logo", required=False, defaultFactory=get_default_logo)


class ICustomTheme(Interface):

    css = schema.Text(title="CSS Text", required=False, default="")


class ILayoutComponents(Interface):

    components = schema.JSONField(
        title="Layout enabled components by type",
        required=False,
        schema=LAYOUT_TYPE_COMPONENTS,
        defaultFactory=dict,
    )
