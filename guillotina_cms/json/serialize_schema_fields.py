from guillotina import configure
from guillotina.schema.interfaces import IChoice
from guillotina.interfaces import ISchemaFieldSerializeToJson
from guillotina.json.serialize_schema_field import DefaultSchemaFieldSerializer
from guillotina.utils import get_object_url
from guillotina.utils import get_current_container
from zope.interface import Interface
from guillotina.schema.interfaces import ISource
from guillotina.schema.vocabulary import SimpleVocabulary


@configure.adapter(
    for_=(IChoice, Interface, Interface),
    provides=ISchemaFieldSerializeToJson)
class DefaultChoiceSchemaFieldSerializer(DefaultSchemaFieldSerializer):

    def serialize(self):
        result = super(DefaultChoiceSchemaFieldSerializer, self).serialize()
        if self.field.vocabularyName is not None:
            container = get_current_container()
            result['vocabulary'] = {
                '@id': get_object_url(container, self.request) + '/@vocabularies/' + self.field.vocabularyName
            }
        else:
            if isinstance(self.field.vocabulary, SimpleVocabulary):
                result['choices'] = [(x.token, x.value) for x in self.field.vocabulary._terms]
                result['enum'] = self.field.vocabulary.by_token.keys()
                result['enumNames'] = self.field.vocabulary.by_value.keys()
            elif ISource.providedBy(self.field.vocabulary):
                result['choices'] = self.field.vocabulary.values
                result['enum'] = self.field.vocabulary.keys()
                result['enumNames'] = [v for k, v in self.field.vocabulary.values]
        return result

    @property
    def field_type(self):
        return 'string'
