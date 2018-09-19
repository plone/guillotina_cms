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


fieldset = fieldset_field  # b/w compat
