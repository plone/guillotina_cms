# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Folder
from guillotina.directives import index
from guillotina_cms.interfaces import IDocument


@configure.contenttype(
    type_name="Document",
    schema=IDocument,
    behaviors=[
        "guillotina.behaviors.dublincore.IDublinCore",
        "guillotina_cms.interfaces.base.ICMSBehavior",
        "guillotina_cms.interfaces.blocks.IBlocks",
    ],
    allowed_types=["Image", "File"],  # dynamically calculated
)
class Document(Folder):
    pass

