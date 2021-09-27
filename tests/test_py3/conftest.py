#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Script-Helpers things for pytest
'''
import pytest
import warnings

from fixtures import *


def pytest_addoption(parser):
    '''
    Add extra options to pytest command. See: ``pytest --help``
    '''
    parser.addoption(
            '--skip-cpu', action='store_true', default=False,
            help='Skip CPU-intensive tests, such as hypothetical.benchmark().')
    parser.addoption(
            '--skip-slow', action='store_true', default=False,
            help='Skip slow/time-intensive tests, such as test.sleep().')


def pytest_collection_modifyitems(config, items):
    '''
    Modify collected test stack.
    '''
    # Add '@pytest.mark.cpu' decorator to test function to invoke skip.
    skip_cpu = pytest.mark.skip(reason='Skip: High CPU')
    # Add '@pytest.mark.slow' decorator to test function to invoke skip.
    skip_slow = pytest.mark.skip(reason='Skip: Long Running')
    # Add '@pytest.mark.broken' decorator to test function to invoke skip.
    skip_broken = pytest.mark.skip(reason='Skip: Broken | ONLY FOR DEVELOPING TESTS')

    for item in items:
        if 'broken' in item.keywords:
            warnings.warn(UserWarning('WARNING: BROKEN TEST(S) SKIPPED'))
            item.add_marker(skip_broken)
        if 'cpu' in item.keywords and config.getoption('--skip-cpu'):
            item.add_marker(skip_cpu)
        if 'slow' in item.keywords and config.getoption('--skip-slow'):
            item.add_marker(skip_slow)
