from guillotina import schema
from guillotina_cms import configure_cms
from zope.interface import Interface
from guillotina.schema import JSONField
import json


@configure_cms.block(
    name='title', title='title'
)
class IBlockTitle(Interface):
    title = schema.TextLine(required=True)


@configure_cms.block(
    name='description', title='Description'
)
class IBlockDescription(Interface):
    description = schema.TextLine(required=True)


TEXT_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'content-type': {'type': 'string'},
        'text': {'type': 'string'},
        'data': {'type': 'string'}
    }
})


@configure_cms.block(
    name='text', title='Text'
)
class IBlockText(Interface):
    text = JSONField(
        schema=TEXT_SCHEMA
    )

    description = schema.TextLine()


@configure_cms.block(
    name='image', title='Image'
)
class IBlockImage(Interface):
    url = schema.TextLine()


@configure_cms.block(
    name='video', title='Video'
)
class IBlockVideo(Interface):
    url = schema.TextLine()
