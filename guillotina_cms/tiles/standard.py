from guillotina import schema
from guillotina_cms import configure_cms
from zope.interface import Interface
from guillotina.schema import JSONField
import json


@configure_cms.tile(
    name='title', title='title'
)
class ITileTitle(Interface):
    title = schema.TextLine(required=True)


@configure_cms.tile(
    name='description', title='Description'
)
class ITileDescription(Interface):
    description = schema.TextLine(required=True)


TEXT_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'content-type': {'type': 'string'},
        'text': {'type': 'string'},
        'data': {'type': 'string'}
    }
})


@configure_cms.tile(
    name='text', title='Text'
)
class ITileText(Interface):
    text = JSONField(
        schema=TEXT_SCHEMA
    )

    description = schema.TextLine()


@configure_cms.tile(
    name='image', title='Image'
)
class ITileImage(Interface):
    url = schema.TextLine()


@configure_cms.tile(
    name='video', title='Video'
)
class ITileVideo(Interface):
    url = schema.TextLine()
