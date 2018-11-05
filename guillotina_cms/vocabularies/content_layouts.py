from guillotina import configure
from guillotina import app_settings


@configure.vocabulary(
    name="content_layouts")
class ContentLayoutVocabulary:

    def __init__(self, context):
        self.context = context
        if hasattr(self.context, 'context'):
            main_interface = [x for x in self.context.context.__provides__][0].__identifier__
        else:
            main_interface = [x for x in self.context.__provides__][0].__identifier__
        self.values = app_settings['layouts'].get(main_interface, [])

    def keys(self):
        return self.values

    def __iter__(self):
        return iter([x for x in self.values])

    def __contains__(self, value):
        return value in self.values

    def __len__(self):
        return len(self.values)

    def getTerm(self, value):
        if value in self.values:
            return value
        else:
            raise KeyError('No valid state')
