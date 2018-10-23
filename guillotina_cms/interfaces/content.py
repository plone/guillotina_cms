from guillotina.fields import CloudFileField
from guillotina.interfaces import IFolder
from guillotina.interfaces import IItem
from guillotina_cms.directives import fieldset_field
from guillotina_cms.fields.image import CloudImageFileField
from guillotina_cms.fields.richtext import RichTextField
from guillotina_cms.interfaces.image import IHasImage


class IDocument(IFolder):

    fieldset_field('text', 'default')
    text = RichTextField(
        title='Text',
        required=False,
        widget='richtext')

class IImage(IItem, IHasImage):

    fieldset_field('image', 'default')
    image = CloudImageFileField(
        title='Image',
        required=False,
        widget='file')

class IFile(IItem):

    fieldset_field('file', 'default')
    file = CloudFileField(
        title='File',
        required=False,
        widget='file')


class INews(IItem):

    fieldset_field('text', 'default')
    text = RichTextField(
        title='Text',
        required=False,
        widget='richtext')
