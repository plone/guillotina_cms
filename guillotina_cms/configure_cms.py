from guillotina.configure import _base_decorator
from guillotina.configure import register_configuration_handler
from guillotina_cms import app_settings


def load_tiletype(_context, tile):
    config = tile['config']
    app_settings['available_tiles'][config['name']] = {
        'title': config['title'],
        'name': config['name'],
        'add_permission': config.get('add_permission', 'guillotina.AddContent'),
        'view_permission': config.get('view_permission', 'guillotina.ViewContent'),
        'edit_permission': config.get('edit_permission', 'guillotina.ModifyContent'),
        'description': config.get('description', ''),
        'icon': config.get('icon', 'default'),
        'schema': tile['klass']
    }

register_configuration_handler('tile', load_tiletype) # noqa


class tile(_base_decorator):  # noqa: N801
    configuration_type = 'tile'
