from zope.interface import Interface
from guillotina import schema
from guillotina.directives import index_field
from guillotina.directives import read_permission
from guillotina.directives import write_permission


class IFollowingMarker(Interface):
    """Marker interface for following."""


class IFollowing(Interface):

    index_field('favorites', type='keyword', store=True)

    read_permission(favorites='guillotina.')
    write_permission(favorites='guillotina.NoBody')
    favorites = schema.List(
        title=u'favorites',
        default=[],
        value_type=schema.TextLine(title='follower'))

    favorite = schema.Bool(
        title=u'Current user has it favorited',
        default=False)
