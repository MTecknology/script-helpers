#!/usr/bin/env python3
'''
..
    Title: Script Helpers (py3)
    Copyright: 2021 Michael Lustfield <MTecknology>
    License: GPL-3+
    Ref: https://script-helpers.readthedocs.io/en/latest/helpers/python3.html
    Usage: https://script-helpers.readthedocs.io/en/latest/samples/python3.html

Py3Helpers provides a library of "helper" functions and classes to help reduce
errors caused by copy/pasting source which is not understood/reviewed.

Usage:

.. code-block:: python

    sys.path.append('/path/to/helper/libs')
    import py3helpers

    py3helpers.collapse_integers([1,2,3])
'''
# Standard Library Imports
import itertools


def collapse_integers(input_list):
    '''
    Return a string of collapsed ranges from a sorted list|set of integers.

    input_list
        List of integers to be collapsed (input is sorted/de-duped)

    >>> collapse_integers(set([1, 2, 3, 4, 5, 8, 9, 11, 12, 13, 14]))
    '1-5,8-9,11-14'
    >>> collapse_integers([])
    ''
    '''
    # Sanitize input
    input_set = sorted(set(input_list))

    def _torange(i):
        l = list(i)
        if len(l) > 1:
            return f'{l[0]}-{l[-1]}'
        else:
            return f'{l[0]}'

    return ','.join(
            _torange(g) for _, g in
            itertools.groupby(
                input_set,
                key=lambda n,
                c=itertools.count(): n-next(c)))
