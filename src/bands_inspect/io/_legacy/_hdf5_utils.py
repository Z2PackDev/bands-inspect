# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <mail@greschd.ch>
"""
Helper functions for serializing objects to HDF5.
"""


def nested_list_from_hdf5(hdf5_handle):
    res = []
    for idx in sorted(hdf5_handle, key=int):
        res.append(list(hdf5_handle[idx][()]))
    return _decode_bytes_nested(res)


def _decode_bytes_nested(val):  # pylint: disable=missing-function-docstring
    if isinstance(val, bytes):
        return val.decode("utf-8")
    if isinstance(val, list):
        return [_decode_bytes_nested(v) for v in val]
    return val


def dict_from_hdf5(hdf5_handle):
    res = {}
    for key in hdf5_handle:
        res[key] = hdf5_handle[key][()]
    return res
