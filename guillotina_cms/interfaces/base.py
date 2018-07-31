from zope.interface import Interface
from guillotina import schema
from guillotina.directives import index


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

    index('review_state', type='keyword')
    review_state = schema.Choice(
        title='Workflow review state',
        required=False,
        source='worklow_states')
