from guillotina.directives import Directive


class MetadataDictMergeDirective(Directive):
    """Store a dict value in the tagged value under the key.
    """
    key: str

    def store(self, tags, value):
        tags.setdefault(self.key, {})
        for key in value.keys():
            if key in tags[self.key]:
                tags[self.key][key].append(value[key])
            else:
                tags[self.key][key] = [value[key]]


class fieldset_field(MetadataDictMergeDirective):  # noqa: N801
    """
    Directive used to set fieldset attributes.
    """
    key = 'guillotina_cms.directives.fieldset'

    def factory(self, name, fieldset):
        return {
            fieldset: name
        }

def merged_tagged_value_dict_merged(iface, name):
    """Look up the tagged value 'name' in schema and all its bases, assuming
    that the value under 'name' is a dict. Return a dict that consists of
    all dict items, with those from more-specific interfaces overriding those
    from more-general ones.
    """
    tv = {}
    for iface in reversed(iface.__iro__):
        value = iface.queryTaggedValue(name, {})
        for key, item in value.items():
            if key in tv:
                tv[key].extend(item)
            else:
                tv[key] = item.copy()
    return tv


fieldset = fieldset_field  # b/w compat
