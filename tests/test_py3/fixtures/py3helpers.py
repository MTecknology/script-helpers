#!/usr/bin/env python3
'''
Test Fixtures: Pp3Helpers
'''
# StdLib Imports
import os
import pytest
import sys

# Our wacky loader
WORKSPACE = os.environ.get('WORKSPACE', '.')
sys.path.append(f'{WORKSPACE}/lib')
import py3helpers


@pytest.fixture
def p3h():
    '''
    Provides the py3helpers object in an easy-to-consume fixture.
    '''
    return py3helpers
