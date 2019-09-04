from guillotina import configure
from guillotina import app_settings
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina.behaviors.properties import ContextProperty
from guillotina_cms.interfaces import ICMSBehavior
from guillotina_cms.interfaces import IWorkflow
from guillotina.utils import iter_parents
from guillotina.interfaces import IFolder


def default_review_state(context=None, name=None):
    return IWorkflow(context).initial_state


def default_layout(context=None, name=None):
    return "document_view"


def default_language(context=None, name=None):
    for parent in iter_parents(context):
        if hasattr(parent, name):
            return parent.name
    return None


@configure.behavior(title="CMS data behavior", provides=ICMSBehavior, for_="guillotina.interfaces.IResource")
class CMS(AnnotationBehavior):

    review_state = ContextProperty("review_state", default_review_state)
    language = ContextProperty("language", default_language)
    content_layout = ContextProperty("content_layout", default_layout)
    position_in_parent = ContextProperty("position_in_parent", -1)
    _allow_discussion = ContextProperty("_allow_discussion", None)

    @property
    def is_folderish(self):
        return IFolder.providedBy(self.context)

    @property
    def allow_discussion(self):
        if self.context.type_name not in app_settings.get("allow_discussion_types", []):
            return False

        if self._allow_discussion is None:
            return app_settings.get("default_allow_discussion")
        return self._allow_discussion

    @allow_discussion.setter
    def set_allow_discussion(self, value):
        self._allow_discussion = value
