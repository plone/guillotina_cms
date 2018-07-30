from guillotina import configure
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina_cms.interfaces import ICMSBehavior
from guillotina_cms.interfaces import IWorkflow
from guillotina.utils import iter_parents


@configure.behavior(
    title="CMS data behavior",
    provides=ICMSBehavior,
    for_="guillotina.interfaces.IResource")
class CMS(AnnotationBehavior):

    def get_language(self):
        if hasattr(self.context, '__language'):
            return self.context.__language
        else:
            for parent in iter_parents(self.context):
                if hasattr(self.context, '__language'):
                    return self.context.__language
            return None

    def set_language(self, value):
        self.context.__review_state__ = value

    def del_language(self):
        del self.context.__review_state

    language = property(
        get_language, set_language, del_language)

    def get_review_state(self):
        if hasattr(self.context, '__review_state'):
            return self.context.__review_state
        else:
            return IWorkflow(self.context).initial_state

    def set_review_state(self, value):
        self.context.__review_state__ = value
        self.context._p_register()

    def del_review_state(self):
        del self.context.__review_state
        self.context._p_register()

    review_state = property(
        get_review_state, set_review_state, del_review_state)
