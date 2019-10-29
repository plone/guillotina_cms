from guillotina import configure
from guillotina import app_settings
from guillotina.interfaces import IResource
from guillotina_cms.interfaces import IDefaultBlocksLayout
from guillotina_cms.interfaces import IDefaultBlocks


@configure.adapter(for_=IResource, provides=IDefaultBlocksLayout)
class DefaultBlocksLayout:
    def __init__(self, context):
        self.context = context

    def __call__(self):
        default_blocks = app_settings.get("default_blocks", None)
        default_result = {"items": []}
        if default_blocks is not None and self.context.type_name in default_blocks:
            return default_blocks[self.context.type_name].get("blocks_layout", default_result)
        else:
            return default_result


@configure.adapter(for_=IResource, provides=IDefaultBlocks)
class DefaultBlocks:
    def __init__(self, context):
        self.context = context

    def __call__(self):
        default_result = {}
        default_blocks = app_settings.get("default_blocks", None)
        if default_blocks is not None and self.context.type_name in default_blocks:
            return default_blocks[self.context.type_name].get("blocks", default_result)
        else:
            return default_result
