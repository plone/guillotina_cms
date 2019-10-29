from guillotina.configure import _base_decorator
from guillotina.configure import register_configuration_handler
from guillotina_cms import app_settings


def load_blocktype(_context, block):
    config = block['config']
    app_settings['available_blocks'][config['name']] = {
        'title': config['title'],
        'name': config['name'],
        'add_permission': config.get('add_permission', 'guillotina.AddContent'),
        'view_permission': config.get('view_permission', 'guillotina.ViewContent'),
        'edit_permission': config.get('edit_permission', 'guillotina.ModifyContent'),
        'description': config.get('description', ''),
        'icon': config.get('icon', 'default'),
        'schema': block['klass']
    }

register_configuration_handler('block', load_blocktype) # noqa


class block(_base_decorator):  # noqa: N801
    configuration_type = 'block'
