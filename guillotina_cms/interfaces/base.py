from zope.interface import Interface
from guillotina import schema
from guillotina.directives import index
import json

HISTORY_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'actor': {'type': 'string'},
        'comments': {'type': 'string'},
        'time': {'type': 'date'},
        'type': {'type': 'string'},
        'title': {'type': 'string'},
        'data': {'type': 'object'}
    }
})

# If its a workflow:
#     type: workflow
#     data:
#         action: string (action)
#         review_state: string (review state moved to)

# If its a versioning:
#     type: versioning
#         version: int (action)


class ICMSLayer(Interface):
    """Marker interface layer Plone.CMS."""


class ICMSBehavior(Interface):

    index('hidden_navigation', type='boolean')
    hidden_navigation = schema.Bool(
        title='Should be hidden on navigation',
        required=False,
        default=False)

    index('language', type='keyword')
    language = schema.Choice(
        title='Language',
        required=False,
        source='languages')

    index('position_in_parent', type='int')
    position = schema.Int(
        title='Position in parent',
        required=False)

    index('review_state', type='keyword')
    review_state = schema.Choice(
        readonly=True,
        title='Workflow review state',
        required=False,
        source='worklow_states')

    history = schema.List(
        title='History list',
        readonly=True,
        required=False,
        value_type=schema.JSONField(
            title='History element',
            schema=HISTORY_SCHEMA))
