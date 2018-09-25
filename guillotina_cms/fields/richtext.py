from guillotina import configure
from guillotina.component import get_adapter
from guillotina.exceptions import ValueDeserializationError
from guillotina.interfaces import IJSONToValue
from guillotina.schema import Object
from guillotina.schema._field import _validate_fields
from guillotina.schema.exceptions import WrongContainedType
from guillotina_cms.fields.interfaces import IRichTextField
from guillotina_cms.fields.interfaces import IRichTextFieldSchema
from zope.interface import implementer


# This class is hacky because the rest api
# uses a subfield on richtext called content-type
# Yes ... with a - ....


class RichTextFieldValue(object):

    content_type = None
    encoding = None
    data = None


@implementer(IRichTextField)
class RichTextField(Object):

    def __init__(self, *args, **kwargs):
        super(RichTextField, self).__init__(
            *args, schema=IRichTextFieldSchema, **kwargs)

    def _validate(self, value):
        if isinstance(value, RichTextFieldValue):
            # check the value against schema
            errors = _validate_fields(IRichTextFieldSchema, value)
        else:
            raise Exception('Not valid field')
        if errors:
            raise WrongContainedType(errors, self.__name__)


@configure.value_deserializer(IRichTextField)
def field_deserializer(field, value, context):
    if not isinstance(value, dict):
        raise ValueDeserializationError(field, value, 'Not an object')
    new_obj = RichTextFieldValue()
    for key, val in value.items():
        if key == 'content-type':
            key = 'content_type'
        if key in field.schema:
            f = field.schema[key]

            if val is not None:
                setattr(
                    new_obj, key,
                    get_adapter(f, IJSONToValue, args=[val, context]))
            else:
                setattr(new_obj, key, None)
    return new_obj


@configure.value_serializer(RichTextFieldValue)
def field_serializer(field):
    return {
        'content-type': field.content_type,
        'data': field.data,
        'encoding': field.encoding
    }
