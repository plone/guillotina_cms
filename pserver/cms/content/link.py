# -*- encoding: utf-8 -*-
from plone.server.content import Item
from plone.server.interfaces import IItem
from zope.interface import implementer
from zope import schema
from pserver.cms import _
from plone.supermodel.directives import catalog


class ILink(IItem):

    catalog(title='text')
    title = schema.TextLine(
        title=_('Títle'),
        required=False)

    catalog(description='text')
    description = schema.Text(
        title=_('Description'),
        required=False)

    catalog(url='text')
    url = schema.TextLine(
        title=_('URL'),
        required=False)


@implementer(ILink)
class Link(Item):
    pass
