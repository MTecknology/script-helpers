#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Load available fixtures from fixtures/ directory.
'''
# Python / Flask Imports
import os
import importlib
import inspect
import sys

self = sys.modules[__name__]
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for fname in os.listdir('{}/fixtures/'.format(base)):
    if fname == '__init__.py' or fname[-3:] != '.py':
        continue
    mod = importlib.import_module('fixtures.{}'.format(fname[:-3]))

    for nam, fun in inspect.getmembers(mod, inspect.isfunction):
        if hasattr(self, nam):
            pass
        setattr(self, nam, fun)
