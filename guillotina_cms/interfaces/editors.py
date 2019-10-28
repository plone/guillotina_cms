from guillotina import schema
from zope.interface import Interface
import json
from guillotina.directives import index
from guillotina_cms.directives import fieldset_field


GUTENBERG_SCHEMA = json.dumps({"type": "object", "properties": {}})


class IGutenbergMarker(Interface):
    pass


class IGutenberg(Interface):

    fieldset_field("gutenberg", "default")
    gutenberg = schema.List(
        title="Gutenberg list object",
        required=False,
        default=[],
        value_type=schema.JSONField(title="Element Gutenberg", schema=GUTENBERG_SCHEMA),
    )


@index.with_accessor(IGutenbergMarker, "gutenberg", type="searchabletext")
def get_text_from_gutenberg(ob):
    # Richtext is a dict and we only care about the text
    if ob.gutenberg is not None:
        return ob.gutenberg


class IRichTextMarker(Interface):
    pass


class IRichText(Interface):

    fieldset_field("text", "default")
    text = schema.List(
        title="Gutenberg list object",
        required=False,
        default=[],
        value_type=schema.JSONField(title="Element Gutenberg", schema=GUTENBERG_SCHEMA),
    )


@index.with_accessor(IRichTextMarker, "text", type="searchabletext")
def get_text_from_richtext(ob):
    # Richtext is a dict and we only care about the text
    if ob.text is not None:
        return ob.text.data
