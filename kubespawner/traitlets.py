"""
Traitlets that are used in Kubespawner
"""
from traitlets import TraitType, TraitError, Dict


class Callable(TraitType):
    """
    A trait which is callable.

    Classes are callable, as are instances
    with a __call__() method.
    """

    info_text = 'a callable'

    def validate(self, obj, value):
        if callable(value):
           return value
        else:
            self.error(obj, value)


class Selector(Dict):
    """
    A trait that is used to match Kuberentes labels

    Extends the Dict trailet.
    """

    @staticmethod
    def depth(d, level=0):
        """Return the depth of the Dictionary
        """
        if not isinstance(d, dict) or not d:
            return level
        return max(Selector.depth(d[k], level + 1) for k in d)

    def validate(self, obj, value):
        value = super(Selector, self).validate(obj, value)
        depth = Selector.depth(value)
        if depth <= 1:
            return value
        else:
            raise TraitError("Depth of the Selector dictionary is {} but it cannot be greater than 1".format(depth))
        value = self.validate_elements(obj, value)
        return value

