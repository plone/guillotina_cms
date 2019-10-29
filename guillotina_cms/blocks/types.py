
from guillotina_cms.interfaces import IBlockType
from zope.interface import implementer


@implementer(IBlockType)
class BlockType(object):
    pass
