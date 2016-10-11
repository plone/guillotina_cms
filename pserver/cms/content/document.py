# -*- encoding: utf-8 -*-
from plone.server.content import Item
from plone.server.interfaces import IItem
from zope.interface import implementer
from zope import schema
from pserver.cms import _
from plone.supermodel.directives import catalog


class IDocument(IItem):

    catalog(title='text')
    title = schema.TextLine(
        title=_('Títle'),
        required=False)

    catalog(description='text')
    description = schema.Text(
        title=_('Description'),
        required=False)

    catalog(text='text')
    text = schema.Text(
        title=_('Text'),
        required=False)


@implementer(IDocument)
class Document(Item):
    pass
