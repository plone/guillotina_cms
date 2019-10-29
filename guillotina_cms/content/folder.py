# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Folder
from guillotina_cms.interfaces import ICMSFolder


@configure.contenttype(
    type_name="CMSFolder",
    schema=ICMSFolder,
    behaviors=[
        "guillotina.behaviors.dublincore.IDublinCore",
        "guillotina_cms.interfaces.base.ICMSBehavior",
        "guillotina_cms.interfaces.blocks.IBlocks",
    ],
)
class CMSFolder(Folder):
    pass
