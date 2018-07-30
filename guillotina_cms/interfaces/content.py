from guillotina.interfaces import IFolder
from guillotina_cms.fields.richtext import RichTextField


class IDocument(IFolder):

    text = RichTextField(
        title='Text',
        required=False,
        widget='richtext')
