import asyncio
import logging
import typing
import json
from guillotina import app_settings
from guillotina_cms.vocabularies.source import AppSettingSource
from guillotina_cms.directives import fieldset_field
from guillotina_cms import dyncontent
from guillotina import configure
from guillotina import FACTORY_CACHE
from guillotina import BEHAVIOR_CACHE

from guillotina.component import get_global_components
from guillotina.component import get_utility
from guillotina.component import query_utility
from guillotina.content import get_cached_factory
from guillotina.content import load_cached_schema
from guillotina.schema.vocabulary import SimpleVocabulary
from guillotina.directives import index_field
from guillotina.directives import metadata
from guillotina.directives import read_permission
from guillotina.directives import write_permission
from guillotina.interfaces import IApplication
from guillotina.interfaces import IBehavior
from guillotina.interfaces import IApplicationInitializedEvent
from guillotina.interfaces import IResourceFactory
from guillotina.utils import import_class
from zope.interface import Interface
from zope.interface.interface import InterfaceClass

SUPPORTED_DIRECTIVES = {
    'fieldset': fieldset_field,
    'index': index_field,
    'read_permission': read_permission,
    'write_permission': write_permission,
    'metadata': metadata
}

logger = logging.getLogger('guillotina_cms')

def get_vocabulary(prop, params):
    # Vocabulary option
    if 'vocabulary' in prop:
        if isinstance(prop['vocabulary'], dict):
            params['vocabulary'] = SimpleVocabulary.fromItems([x for x in prop['vocabulary'].items()])
        elif prop['vocabulary'].startswith('appsettings:'):
            params['source'] = AppSettingSource(
                prop['vocabulary'].replace('appsettings:', '')
            )
        else:
            params['vocabulary'] = prop['vocabulary']


def get_fields(*, properties: typing.Dict[str, typing.Dict]):
    fields = {}
    tags = {}

    for prop_id, prop in properties.items():

        params = {}

        field_class = import_class(prop.get('type'))

        # Vocabulary
        get_vocabulary(prop, params)

        # Required
        params['required'] = prop.get('required', False)

        # Title
        params['title'] = prop.get('title')

        widget = prop.get('widget', None)
        if widget:
            params['widget'] = widget

        # Schema
        schema = prop.get('schema', None)
        if schema:
            params['schema'] = json.dumps(schema)

        # Value type
        value_type = prop.get('value_type', None)
        if value_type:
            value_class = import_class(value_type)
            params['value_type'] = value_class(
                required=False,
                title=params['title'] + ' value')

        # Default
        if prop.get('default', None) is not None:
            params['default'] = prop.get('default')

        # Index
        index = prop.get('index', None)
        if index:
            tags.setdefault(prop_id, {})['index'] = index

        write_permission = prop.get('write_permission', None)
        if write_permission:
            tags.setdefault(prop_id, {})['write_permission'] = write_permission

        metadata = prop.get('metadata', None)
        if metadata:
            tags.setdefault(prop_id, {})['metadata'] = None

        read_permission = prop.get('read_permission', None)
        if read_permission:
            tags.setdefault(prop_id, {})['read_permission'] = read_permission

        fields[prop_id] = field_class(**params)

    #
    return fields, tags


def create_content_factory(proto_name, proto_definition):
    parent_interface = import_class(proto_definition.get(
        'inherited_interface',
        'guillotina.interfaces.content.IFolder'))
    parent_class = import_class(proto_definition.get(
        'inherited_class',
        'guillotina.content.Folder'))

    schema_fields, tags = get_fields(
        properties=proto_definition.get('properties'))

    for fieldset_id, fieldset_list in proto_definition.get('fieldsets', {}).items():
        for field_id in fieldset_list:
            tags.setdefault(field_id, {})['fieldset'] = fieldset_id

    class_interface = InterfaceClass(
        'I' + proto_name,
        (parent_interface,),
        schema_fields,
        __module__='guillotina_cms.interfaces')

    for field_id, tag in tags.items():
        for tag_id, tag_metadata in tag.items():
            if tag_id in SUPPORTED_DIRECTIVES:
                if tag_metadata is None:
                    SUPPORTED_DIRECTIVES[tag_id].apply(class_interface, field_id)
                elif isinstance(tag_metadata, dict):
                    SUPPORTED_DIRECTIVES[tag_id].apply(class_interface, field_id, **tag_metadata)
                elif isinstance(tag_metadata, list):
                    SUPPORTED_DIRECTIVES[tag_id].apply(class_interface, field_id, *tag_metadata)
                elif tag_id == 'fieldset':
                    SUPPORTED_DIRECTIVES[tag_id].apply(class_interface, field_id, tag_metadata)
                elif isinstance(tag_metadata, str):
                    SUPPORTED_DIRECTIVES[tag_id].apply(class_interface, **{
                        field_id: tag_metadata})

    klass = type(
        proto_name,
        (parent_class,),
        {})

    klass.__module__ = 'guillotina_cms.dyncontent'
    setattr(dyncontent, proto_name, klass)

    behaviors = []
    for bhr in proto_definition.get('behaviors', []):
        if bhr in BEHAVIOR_CACHE:
            behaviors.append(BEHAVIOR_CACHE[bhr])
        else:
            raise Exception(f"Behavior not found {bhr}")

    contenttype = {
        'schema': class_interface,
        'type_name': proto_name,
        'allowed_types': proto_definition.get('allowed_types', []),
        'add_permission': proto_definition.get('add_permission', 'guillotina.AddContent'),
        'behaviors': behaviors
    }

    utility = query_utility(IResourceFactory, name=proto_name)
    if utility is not None:
        sm = get_global_components()
        sm.unregisterUtility(utility, IResourceFactory, proto_name)

    configure.register_configuration(klass, contenttype, 'contenttype')

    root = get_utility(IApplication, name='root')
    configure.load_configuration(
        root.app.config, 'guillotina_cms.dyncontent', 'contenttype')
    root.app.config.execute_actions()
    configure.clear()
    load_cached_schema()

    # Verify its created
    if proto_name in FACTORY_CACHE:
        del FACTORY_CACHE[proto_name]
    get_cached_factory(proto_name)


def create_behaviors_factory(proto_name, proto_definition):

    if proto_definition.get('for', None) is None:
        raise Exception('We need a for interface')
    else:
        for_ = import_class(proto_definition.get('for'))

    if for_ is None:
        raise Exception('Wrong for interface')

    parent_class = import_class(proto_definition.get(
        'inherited_class',
        'guillotina.behaviors.instance.AnnotationBehavior'))

    schema_fields, tags = get_fields(
        properties=proto_definition.get('properties'))

    base_interface = proto_definition.get('base_interface', None)
    if base_interface is None:
        base_interface = Interface

    class_interface = InterfaceClass(
        'I' + proto_name,
        (base_interface,),
        schema_fields,
        __module__='guillotina_cms.interfaces')

    for field_id, tag in tags.items():
        for tag_id, tag_metadata in tag.items():
            if tag_id in SUPPORTED_DIRECTIVES:
                SUPPORTED_DIRECTIVES[tag_id].apply(class_interface, field_id, tag_metadata)

    klass = type(
        proto_name,
        (parent_class,),
        {})

    klass.__module__ = 'guillotina_cms.behaviors'

    behavior = {
        'for_': for_,
        'provides': class_interface,
        'data_key': proto_definition.get('data_key', 'default'),
        'auto_serialize': proto_definition.get('auto_serialize', True),
        'name': proto_name,
        'name_only': proto_definition.get('name_only', False),
        'title': proto_definition.get('title', ''),
        'marker': proto_definition.get('marker', None),
        'description': proto_definition.get('description', '')
    }

    configure.register_configuration(klass, behavior, 'behavior')

    root = get_utility(IApplication, name='root')
    configure.load_configuration(
        root.app.config, 'guillotina_cms.behaviors', 'behavior')
    root.app.config.execute_actions()
    configure.clear()
    load_cached_schema()

    # Verify its created
    interface_name = 'guillotina_cms.interfaces.I' + proto_name
    utility = get_utility(IBehavior, name=interface_name)
    interface_name = 'guillotina_cms.interfaces.I' + proto_name
    utility2 = get_utility(IBehavior, name=proto_name)
    assert BEHAVIOR_CACHE[interface_name] == class_interface
    utility.interface == class_interface
    utility2.interface == class_interface


@configure.subscriber(for_=IApplicationInitializedEvent)
async def add_initialized(event):
    for type_name, definition in app_settings.get('behaviors', {}).items():
        create_behaviors_factory(type_name, definition)
    for type_name, definition in app_settings.get('contents', {}).items():
        create_content_factory(type_name, definition)

