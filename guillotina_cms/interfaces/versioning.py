from zope.interface import Interface
from guillotina.fields.annotation import BucketListField


class IVersioning(Interface):
    diffs = BucketListField(
        readonly=True,
        annotation_prefix='diffs-',
        bucket_len=5
    )

class IVersioningMarker(Interface):
    """Marker interface an object is Versioning"""

class IDiffCalculator(Interface):
    """Interface for an adapter to look for diffs"""

    async def __call__(payload):
        pass
