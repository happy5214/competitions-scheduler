# -*- coding: utf-8  -*-
"""Package for tests."""

from __future__ import unicode_literals

import unittest


class TestCase(unittest.TestCase):

    """Subclass of unittest.TestCase."""

    if not hasattr(unittest.TestCase, 'assertCountEqual'):

        def assertCountEqual(self, *args, **kwargs):
            """Wrapper of assertItemsEqual()."""
            return self.assertItemsEqual(*args, **kwargs)
