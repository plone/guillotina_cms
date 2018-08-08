from zope.interface import Interface
from guillotina import schema
from guillotina.directives import index
from guillotina.fields import BucketListField
import json

HISTORY_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'action': 'string',
        'actor': {'type': 'string'},
        'comments': {'type': 'string'},
        'review_state': {'type': 'string'},
        'time': {'type': 'date'},
        'title': {'type': 'string'}
    }
})


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
        title='Workflow review state',
        required=False,
        source='worklow_states')

    history = BucketListField(
        title='History list',
        required=False,
        value_type=schema.JSONField(
            title='History element',
            schema=HISTORY_SCHEMA))
