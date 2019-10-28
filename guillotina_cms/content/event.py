# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Item
from guillotina_cms.interfaces import IEvent


@configure.contenttype(
    type_name="Event",
    schema=IEvent,
    behaviors=[
        "guillotina.behaviors.dublincore.IDublinCore",
        "guillotina_cms.interfaces.base.ICMSBehavior",
    ],
    allowed_types=["Image", "File"],  # dynamically calculated
)
class Event(Item):
    pass

