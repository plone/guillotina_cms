from guillotina import configure
from guillotina.interfaces import IIDGenerator
from guillotina_cms.interfaces import ICMSLayer


@configure.adapter(
    for_=(ICMSLayer),
    provides=IIDGenerator)
class IDGenerator(object):
    """Default IDGenerator adapter.

    Requires request to adapt on different layers. Returns the urls path id.
    """

    def __init__(self, request):
        self.request = request

    def __call__(self, data):

        if 'title' in data:
            new_title = data['title'].lower().replace(' ', '-')
            return new_title
        if '@type' in data and data['@type'] == 'Image':
            try:
                return data['image']['filename']
            except KeyError:
                return None
        else:
            return None
