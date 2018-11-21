# -*- coding: utf-8 -*-
from guillotina.i18n import MessageFactory
from guillotina import configure
import glob
import yaml

_ = MessageFactory('guillotina_cms')


app_settings = {
    'applications': [
        'guillotina_swagger',
        'guillotina_rediscache'
    ],
    'available_tiles': {},
    'pubsub_connector': 'guillotina_cms.pubsub.RedisPubSubConnector',
    'commands': {
        'upgrade': 'guillotina_cms.commands.upgrade.UpgradeCommand'
    },
    'load_utilities': {
        'guillotina_cms.workflow': {
            'provides': 'guillotina_cms.interfaces.IWorkflowUtility',
            'factory': 'guillotina_cms.utilities.workflow.WorkflowUtility',
            'settings': {}
        },
        'guillotina_cms.pubsub': {
            'provides': 'guillotina_cms.interfaces.IPubSubUtility',
            'factory': 'guillotina_cms.utilities.pubsub.PubSubUtility',
            'settings': {}
        }
    },
    'layouts': {
        'guillotina.interfaces.content.IFolder': [
            'listing_view',
            'tabular_view',
            'summary_view',
            'layout_view',
            'full_view',
            'album_view',
            'event_listing'
        ],
        'guillotina_cms.interfaces.content.IDocument': [
            'document_view',
            'layout_view'
        ],
        'guillotina_cms.interfaces.content.INews': [
            'document_view',
            'layout_view'
        ],
        'guillotina_cms.interfaces.content.IEvent': [
            'document_view',
            'layout_view'
        ],
        'guillotina_cms.interfaces.content.ILink': [
            'document_view',
            'layout_view'
        ],
        'guillotina_cms.interfaces.content.IFile': [
            'document_view',
            'layout_view'
        ]
    },
    'workflows': {
        'private': {
            'initial_state': 'private',
            'states': {
                'private': {
                    'set_permission': {},
                    'actions': {}
                }
            }
        },
        'basic': {
            'initial_state': 'private',
            'states': {
                'private': {
                    'actions': {
                        'publish': {
                            'title': 'Publish',
                            'to': 'public',
                            'check_permission': 'guillotina.ReviewContent'
                        }
                    },
                    'set_permission': {
                        'roleperm': [
                            {
                                'setting': 'Deny',
                                'role': 'guillotina.Anonymous',
                                'permission': 'guillotina.ViewContent'
                            },
                            {
                                'setting': 'Deny',
                                'role': 'guillotina.Anonymous',
                                'permission': 'guillotina.AccessContent'
                            }
                        ]
                    }
                },
                'public': {
                    'actions': {
                        'retire': {
                            'title': 'Retire',
                            'to': 'private',
                            'check_permission': 'guillotina.ReviewContent'
                        }
                    },
                    'set_permission': {
                        'roleperm': [
                            {
                                'setting': 'AllowSingle',
                                'role': 'guillotina.Anonymous',
                                'permission': 'guillotina.ViewContent'
                            },
                            {
                                'setting': 'AllowSingle',
                                'role': 'guillotina.Anonymous',
                                'permission': 'guillotina.AccessContent'
                            }
                        ]
                    }
                }
            }
        }
    },
    'workflows_content': {
        'guillotina.interfaces.IResource': 'private',
        'guillotina.interfaces.IContainer': 'basic',
        'guillotina_cms.content.document.IDocument': 'basic'
    },
    'search_parser': 'guillotina_cms.search.parser.Parser',
    'default_tiles': {
        'Document': [
            {'type': 'title'},
            {'type': 'text'}
        ]
    }
}

path = '/'.join(__file__.split('/')[:-1])

for workflow_file in glob.glob(path + '/workflows/*.yaml'):
    with open(workflow_file, 'r') as f:
        workflow_content = yaml.load(f)
    ident = workflow_file.split('/')[-1].rstrip('.yaml')
    app_settings['workflows'][ident] = workflow_content

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
    configure.scan('guillotina_cms.subscribers')
    configure.scan('guillotina_cms.tiles')
