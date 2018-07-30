# -*- coding: utf-8 -*-
from guillotina.i18n import MessageFactory
from guillotina import configure

_ = MessageFactory('guillotina_cms')


app_settings = {
    'available_tiles': {},
    'pubsub_connector': 'guillotina_cms.pubsub.RedisPubSubConnector',
    'commands': {
        'upgrade': 'guillotina_cms.commands.upgrade.UpgradeCommand'
    },
    'workflows': {
        'basic': {
            'initial_state': 'private',
            'states': {
                'private': {}
            }
        }
    },
    'workflows_content': {
        'guillotina.interfaces.IResource': 'basic'
    },
    'search_parser': 'guillotina_cms.search.parser.Parser'
}


def includeme(root):
    configure.scan('guillotina_cms.interfaces')
    configure.scan('guillotina_cms.api')
    configure.scan('guillotina_cms.behaviors')
    configure.scan('guillotina_cms.content')
    configure.scan('guillotina_cms.fields')
    configure.scan('guillotina_cms.json')
    configure.scan('guillotina_cms.utilities')
    configure.scan('guillotina_cms.vocabularies')
    configure.scan('guillotina_cms.permissions')
    configure.scan('guillotina_cms.install')
    configure.scan('guillotina_cms.validator')
    configure.scan('guillotina_cms.tiles')
