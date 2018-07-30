import logging
from guillotina import app_settings
from guillotina_cms.interfaces import IWorkflowUtility
from guillotina_cms.interfaces import IWorkflow
from guillotina import configure
from guillotina.component import provide_adapter
from guillotina.utils import import_class


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
        def initial_state(self):
            return self._initial_state

        async def switch_state(self, action):
            pass
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
