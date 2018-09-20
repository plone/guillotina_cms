from guillotina import schema
from zope.interface import Interface


class IImagingSettings(Interface):
    allowed_sizes = schema.Dict(
        missing_value={
            'high': '1400:1400',
            'large': '768:768',
            'preview': '400:400',
            'mini': '200:200',
            'thumb': '128:128',
            'tile': '64:64',
            'icon': '32:32'
        })

    quality = schema.Int(default=88)
