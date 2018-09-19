from guillotina.behaviors.dublincore import IDublinCore
from guillotina.interfaces import IResource
from guillotina_cms import directives

directives.fieldset_field.apply(IDublinCore, 'description', 'default')  # pylint: disable=E1101
directives.fieldset_field.apply(IDublinCore, 'effective_date', 'dates')  # pylint: disable=E1101
directives.fieldset_field.apply(IDublinCore, 'expiration_date', 'dates')  # pylint: disable=E1101
directives.fieldset_field.apply(IDublinCore, 'creators', 'ownership')  # pylint: disable=E1101
directives.fieldset_field.apply(IDublinCore, 'tags', 'categorization')  # pylint: disable=E1101
directives.fieldset_field.apply(IDublinCore, 'publisher', 'ownership')  # pylint: disable=E1101
directives.fieldset_field.apply(IDublinCore, 'contributors', 'ownership')  # pylint: disable=E1101
directives.fieldset_field.apply(IResource, '__name__', 'settings')  # pylint: disable=E1101
directives.fieldset_field.apply(IResource, 'title', 'default')  # pylint: disable=E1101
