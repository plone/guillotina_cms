from guillotina.interfaces import IFolder
from guillotina.interfaces import IItem
from guillotina_cms.fields.richtext import RichTextField
from guillotina.fields import CloudFileField


class IDocument(IFolder):

    text = RichTextField(
        title='Text',
        required=False,
        widget='richtext')

class IImage(IItem):

    image = CloudFileField(
        title='Image',
        required=False,
        widget='image')
