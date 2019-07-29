from guillotina import configure
from guillotina import app_settings
from guillotina.interfaces import IResource
from guillotina_cms.interfaces import IDefaultTilesLayout
from guillotina_cms.interfaces import IDefaultTiles


@configure.adapter(for_=IResource, provides=IDefaultTilesLayout)
class DefaultTilesLayout:
    def __init__(self, context):
        self.context = context

    def __call__(self):
        default_tiles = app_settings.get("default_tiles", None)
        default_result = {"items": []}
        if default_tiles is not None and self.context.type_name in default_tiles:
            return default_tiles[self.context.type_name].get("tiles_layout", default_result)
        else:
            return default_result


@configure.adapter(for_=IResource, provides=IDefaultTiles)
class DefaultTiles:
    def __init__(self, context):
        self.context = context

    def __call__(self):
        default_result = {}
        default_tiles = app_settings.get("default_tiles", None)
        if default_tiles is not None and self.context.type_name in default_tiles:
            return default_tiles[self.context.type_name].get("tiles", default_result)
        else:
            return default_result
