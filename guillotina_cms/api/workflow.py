# from guillotina_cms.interfaces import IObjectWorkflow
from guillotina import configure
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IResource
from guillotina.api.service import Service

# Workflows are defined on the configuration on a JSONField structure
# {
#   private:
#       actions:
#           publish:
#               to: public
#               permission: guillotina.AccessContent
#   public:
#       triggers:
#           setpermission:
#               roleperm:
#                   role: guillotina.Member
#                   perm: guillotina.ViewContent
#           notify: followers
#       actions:
#           retire:
#               to: private
#               permission: guillotina.AccessContent
# }


class Workflow(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@workflow',
    summary='Workflows for a resource',
    responses={
        "200": {
            "description": "Result results on workflows",
            "schema": {
                "properties": {}
            }
        }
    })
class WorkflowGET(Service):

    async def __call__(self):
        if not hasattr(self, 'value'):
            workflow = {
                'history': [],
                'transitions': []
            }
        else:
            obj_url = IAbsoluteURL(self.context, self.request)()
            workflow = {
                '@id': obj_url + '/@workflow/' + self.workflow_id,
                'items': await self.value()
            }
        return workflow
