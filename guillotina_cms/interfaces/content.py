from guillotina.fields import CloudFileField
from guillotina.interfaces import IFolder
from guillotina.interfaces import IItem
from guillotina_cms.directives import fieldset_field
from guillotina.schema import Datetime
from guillotina.schema import JSONField
from guillotina_cms.fields.image import CloudImageFileField
from guillotina_cms.fields.richtext import RichTextField
from guillotina_cms.interfaces.image import IHasImage
from guillotina.interfaces import IAsyncUtility
import json

RECURRENT_EVENT = json.dumps({"type": "object", "properties": {}})


class IDocument(IFolder):
    pass


class ICMSFolder(IFolder):
    pass


class IImage(IItem, IHasImage):

    fieldset_field("image", "default")
    image = CloudImageFileField(title="Image", required=False, widget="file")


class IFile(IItem):

    fieldset_field("file", "default")
    file = CloudFileField(title="File", required=False, widget="file")


class IEvent(IItem):

    fieldset_field("start_date", "default")
    start_date = Datetime(title="Start date", required=False, widget="datetime")

    fieldset_field("end_date", "default")
    end_date = Datetime(title="Text", required=False, widget="datetime")

    fieldset_field("recurrent", "default")
    recurrent = JSONField(title="Recurrent", required=False, schema=RECURRENT_EVENT)


class IContentUtility(IAsyncUtility):
    pass
