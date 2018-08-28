import logging
import datetime
from guillotina import app_settings
from guillotina_cms.interfaces import IWorkflowUtility
from guillotina_cms.interfaces import IWorkflow
from guillotina import configure
from guillotina.component import provide_adapter
from guillotina.utils import import_class
from guillotina_cms.interfaces.base import ICMSBehavior
from guillotina.interfaces import IInteraction
from guillotina.response import HTTPUnauthorized
from guillotina.utils import get_authenticated_user_id
from guillotina.security.utils import apply_sharing
from guillotina_cms.events import WorkflowChangedEvent
from guillotina.event import notify


logger = logging.getLogger('guillotina_cms')


def create_workflow_factory(proto_name, proto_definition):

    class Workflow:

        name = proto_name
        definition = proto_definition

        def __init__(self, context):
            self.context = context
            self._states = self.definition['states']
            self._initial_state = self.definition['initial_state']

        @property
        def states(self):
            return self._states

        @property
        def actions(self):
            state = ICMSBehavior(self.context).review_state
            return self._states[state]['actions']

        async def available_actions(self, request):
            security = IInteraction(request)
            for action_name, action in self.actions.items():
                add = False
                if 'check_permission' in action and security.check_permission(
                        action['check_permission'], self.context):
                    add = True
                elif 'check_permission' not in action:
                    add = True

                if add:
                    yield action_name, action

        @property
        def initial_state(self):
            return self._initial_state

        async def do_action(self, request, action, comments):
            available_actions = self.actions
            if action not in available_actions:
                raise KeyError('Unavailable action')

            action_def = available_actions[action]
            security = IInteraction(request)
            if 'check_permission' in action_def and not security.check_permission(
                    action_def['check_permission'], self.context):
                raise HTTPUnauthorized()

            # Change permission
            new_state = action_def['to']

            if 'set_permission' in self.states[new_state]:
                await apply_sharing(self.context, self.states[new_state]['set_permission'])

            # Write history
            user = get_authenticated_user_id(request)
            history = {
                'actor': user,
                'comments': comments,
                'time': datetime.datetime.now(),
                'title': action_def['title'],
                'type': 'workflow',
                'data': {
                    'action': action,
                    'review_state': new_state,
                }
            }

            cms_behavior = ICMSBehavior(self.context)
            await cms_behavior.load()
            cms_behavior.review_state = new_state

            cms_behavior.history.append(history)
            cms_behavior._p_register()

            await notify(WorkflowChangedEvent(self.context, self, action, comments))
            return history

    return Workflow


@configure.utility(provides=IWorkflowUtility)
class WorkflowUtility:

    index_count = 0

    def __init__(self, settings={}, loop=None):
        self.loop = loop
        self.workflows = app_settings['workflows']
        self.workflows_content = app_settings['workflows_content']
        self.factories = {}

    async def initialize(self, app):
        self.app = app
        for workflow_name, definition in self.workflows.items():
            factory = create_workflow_factory(workflow_name, definition)
            self.factories[workflow_name] = factory
        for interface_str, workflow in self.workflows_content.items():
            iface = import_class(interface_str)
            provide_adapter(
                self.factories[workflow], adapts=(iface,), provides=IWorkflow)

    async def finalize(self, app):
        self.factories = {}

    def states(self, context):
        return IWorkflow(context).states

    async def switch_state(self, context, action):
        await IWorkflow(context).switch_state(action)
