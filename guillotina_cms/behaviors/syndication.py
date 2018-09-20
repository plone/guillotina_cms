from guillotina import configure
from guillotina import schema
from guillotina_cms.vocabularies.source import AppSettingSource
from zope.interface import Interface
from guillotina.interfaces import IFolder


@configure.behavior(title="Syndication settings", for_=IFolder)
class ISyndicationSettings(Interface):

    max_items = schema.Int(
        title='Maximum items',
        description='Maximum number of items that will be syndicated.',
        default=15)

    sort_on = schema.Choice(
        title='Sort on',
        default='creation_date',
        source=AppSettingSource(
            'syndication.sort_on',
            missing=[
                ['creation_date', 'Publication Date'],
                ['effective_date', 'Publication Date'],
                ['modification_date', 'Modification Date']
            ]
        )
    )

    sort_reverse = schema.Bool(
        title='Reverse sort',
        description='Order items in reverse order',
        default=True)

    categories = schema.List(
        title='Categories',
        description='(not used with all feed types)',
        value_type=schema.TextLine(),
        default=[],
        required=False,
        missing_value=[]
    )
