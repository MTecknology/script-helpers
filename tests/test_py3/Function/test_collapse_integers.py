#!/usr/bin/env python3
'''
Run tests for function collapse_integers().
'''

def test_arbitrary_expected_list(p3h):
    assert p3h.collapse_integers([0,1,2,3,4,5,11,12]) == '0-5,11-12'

def test_arbitrary_expected_set(p3h):
    assert p3h.collapse_integers(set([0,1,2,3,4,5,11,12])) == '0-5,11-12'

def test_unordered_list(p3h):
    assert p3h.collapse_integers([2,5,10,3,4]) == '2-5,10'

def test_unordered_list_with_duplicates(p3h):
    assert p3h.collapse_integers([2,5,5,5,10,2,2,3,4]) == '2-5,10'

def test_empty_list(p3h):
    assert p3h.collapse_integers([]) == ''

def test_empty_set(p3h):
    assert p3h.collapse_integers(set()) == ''

def test_no_consecutive(p3h):
    assert p3h.collapse_integers([1,3,5,7,9]) == '1,3,5,7,9'
