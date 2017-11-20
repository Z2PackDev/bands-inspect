"""
Defines the mapping between type tags and serializable classes.
"""

from decorator import decorator

SERIALIZE_MAPPING = {}


def subscribe_serialize(type_tag):
    """
    Class decorator that subscribes the class for serialization, with the given type_tag.
    """

    def inner(cls):  # pylint: disable=missing-docstring
        SERIALIZE_MAPPING[type_tag] = cls

        @decorator
        def set_type_tag(to_hdf5_func, self, hdf5_handle):
            hdf5_handle['type_tag'] = type_tag
            return to_hdf5_func(self, hdf5_handle)

        cls.to_hdf5 = set_type_tag(cls.to_hdf5)  # pylint: disable=no-value-for-parameter

        @decorator
        def check_type_tag(from_hdf5_func, cls, hdf5_handle):
            assert hdf5_handle['type_tag'].value == type_tag
            return from_hdf5_func(cls, hdf5_handle)

        cls.from_hdf5 = classmethod(check_type_tag(cls.from_hdf5.__func__))  # pylint: disable=no-value-for-parameter
        return cls

    return inner
