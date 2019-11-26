from guillotina import schema
from zope.interface import Interface
import json
from guillotina_cms.directives import fieldset_field
from guillotina_cms.fields import RichTextField


GUTENBERG_SCHEMA = json.dumps({"type": "object", "properties": {}})
REACT_PAGE_LAYOUT = json.dumps({"type": "object", "properties": {}})


class IGutenberg(Interface):

    fieldset_field("gutenberg", "default")
    gutenberg = schema.List(
        title="Gutenberg list object",
        required=False,
        default=[],
        value_type=schema.JSONField(title="Element Gutenberg", schema=GUTENBERG_SCHEMA),
    )


class IRichText(Interface):

    fieldset_field("text", "default")
    text = RichTextField(
        title="RichText field",
        required=False
    )


class IReactPageLayout(Interface):

    fieldset_field("layout", "default")
    layout = schema.JSONField(
        title="Layout field",
        required=False,
        schema=REACT_PAGE_LAYOUT
    )



