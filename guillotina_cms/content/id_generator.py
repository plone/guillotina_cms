from guillotina import configure
from guillotina.interfaces import IIDGenerator
from guillotina.utils.content import _valid_id_characters
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
            new_id = data['title'].lower().replace(' ', '-')
        elif '@type' in data and data['@type'] == 'Image':
            try:
                new_id = data['image']['filename']
            except KeyError:
                return None
        elif '@type' in data and data['@type'] == 'File':
            try:
                new_id = data['file']['filename']
            except KeyError:
                return None
        else:
            return None
        if new_id[0] in ('_', '@'):
            new_id = new_id[1:]
        return ''.join(
            l for l in new_id
            if l in _valid_id_characters
        )
