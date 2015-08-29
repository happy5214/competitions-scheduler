# -*- coding: utf-8  -*-
"""Tests for round-robin schedulers."""

# Copyright (C) 2015 Alexander Jones
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import random
import sys

from . import TestCase

from competitions.scheduler import ScheduleGenerationFailed
from competitions.scheduler.roundrobin import (
    DoubleRoundRobinScheduler,
    QuadrupleRoundRobinScheduler
)


class TestDoubleRoundRobin(TestCase):

    """Tests for double round-robin scheduling."""

    def test_match_generation(self):
        """Test double round-robin match generation."""
        # Four teams
        scheduler = DoubleRoundRobinScheduler(4)
        expected_matches = [
            (1, 2), (1, 3), (1, 4),
            (2, 1), (2, 3), (2, 4),
            (3, 1), (3, 2), (3, 4),
            (4, 1), (4, 2), (4, 3)
        ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for double '
                               'round-robin schedule with four teams.'))
        # Three teams
        scheduler = DoubleRoundRobinScheduler(3)
        expected_matches = [
            (1, 2), (1, 3), (1, None),
            (2, 1), (2, 3), (2, None),
            (3, 1), (3, 2), (3, None),
            (None, 1), (None, 2), (None, 3)
        ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for double '
                               'round-robin schedule with three teams.'))
        # Eight teams
        scheduler = DoubleRoundRobinScheduler(8)
        expected_matches = [
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 1), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
            (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
            (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8),
            (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8),
            (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8),
            (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8),
            (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7)
        ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for double '
                               'round-robin schedule with eight teams.'))

    def test_schedule_generation(self):
        """Test double round-robin schedule generation."""
        scheduler = DoubleRoundRobinScheduler(8)
        # Failed attempt
        random.seed(5)
        self.assertRaises(ScheduleGenerationFailed,
                          scheduler.generate_schedule, try_once=True)
        # Successful attempt
        random.seed(2)
        if sys.version_info.major == 2:
            expected_schedule = [
                [(5, 6), (7, 4), (3, 8), (1, 2)],
                [(5, 1), (8, 4), (3, 6), (2, 7)],
                [(3, 1), (6, 5), (4, 8), (7, 2)],
                [(8, 5), (3, 2), (1, 4), (7, 6)],
                [(1, 8), (7, 3), (2, 6), (4, 5)],
                [(8, 1), (6, 3), (5, 7), (4, 2)],
                [(6, 1), (2, 5), (4, 3), (8, 7)],
                [(2, 4), (6, 8), (7, 5), (1, 3)],
                [(5, 4), (2, 1), (8, 6), (3, 7)],
                [(4, 7), (2, 8), (3, 5), (1, 6)],
                [(4, 6), (1, 7), (2, 3), (5, 8)],
                [(5, 3), (7, 8), (6, 2), (4, 1)],
                [(7, 1), (5, 2), (6, 4), (8, 3)],
                [(1, 5), (3, 4), (8, 2), (6, 7)]
            ]
        else:
            expected_schedule = [
                [(3, 2), (4, 1), (8, 5), (6, 7)],
                [(3, 8), (1, 6), (7, 5), (2, 4)],
                [(6, 8), (4, 7), (2, 3), (5, 1)],
                [(2, 1), (5, 7), (3, 6), (8, 4)],
                [(5, 4), (6, 2), (3, 7), (1, 8)],
                [(4, 3), (7, 2), (5, 6), (8, 1)],
                [(3, 1), (5, 2), (8, 6), (7, 4)],
                [(7, 1), (6, 4), (5, 3), (2, 8)],
                [(8, 7), (4, 6), (3, 5), (1, 2)],
                [(3, 4), (7, 8), (6, 1), (2, 5)],
                [(1, 4), (7, 3), (5, 8), (2, 6)],
                [(1, 3), (2, 7), (4, 8), (6, 5)],
                [(4, 5), (8, 2), (6, 3), (1, 7)],
                [(1, 5), (4, 2), (7, 6), (8, 3)]
            ]
        schedule = scheduler.generate_schedule(try_once=True)
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for '
                              'double round-robin competition'))


class TestQuadrupleRoundRobin(TestCase):

    """Tests for quadruple round-robin scheduling."""

    def test_match_generation(self):
        """Test quadruple round-robin match generation."""
        # Four teams
        scheduler = QuadrupleRoundRobinScheduler(4)
        expected_matches = [
            (1, 2), (1, 3), (1, 4), (1, 2), (1, 3), (1, 4),
            (2, 1), (2, 3), (2, 4), (2, 1), (2, 3), (2, 4),
            (3, 1), (3, 2), (3, 4), (3, 1), (3, 2), (3, 4),
            (4, 1), (4, 2), (4, 3), (4, 1), (4, 2), (4, 3)
        ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for quadruple '
                               'round-robin schedule with four teams.'))
        # Three teams
        scheduler = QuadrupleRoundRobinScheduler(3)
        expected_matches = [
            (1, 2), (1, 3), (1, None), (1, 2), (1, 3), (1, None),
            (2, 1), (2, 3), (2, None), (2, 1), (2, 3), (2, None),
            (3, 1), (3, 2), (3, None), (3, 1), (3, 2), (3, None),
            (None, 1), (None, 2), (None, 3), (None, 1), (None, 2), (None, 3)
        ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for quadruple '
                               'round-robin schedule with three teams.'))
        # Eight teams
        scheduler = QuadrupleRoundRobinScheduler(8)
        expected_matches = [
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 1), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
            (2, 1), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
            (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
            (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
            (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8),
            (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8),
            (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8),
            (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8),
            (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8),
            (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8),
            (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8),
            (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8),
            (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7),
            (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7)
        ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for quadruple '
                               'round-robin schedule with eight teams.'))

    def test_schedule_generation(self):
        """Test quadruple round-robin schedule generation."""
        scheduler = QuadrupleRoundRobinScheduler(6)
        # Failed attempt
        random.seed(4)
        self.assertRaises(ScheduleGenerationFailed,
                          scheduler.generate_schedule, try_once=True)
        # Successful attempt
        random.seed(1)
        if sys.version_info.major == 2:
            expected_schedule = [
                [(5, 2), (6, 1), (4, 3)],
                [(1, 2), (3, 5), (4, 6)],
                [(5, 6), (3, 1), (4, 2)],
                [(4, 6), (1, 5), (2, 3)],
                [(2, 6), (5, 3), (4, 1)],
                [(2, 5), (3, 4), (6, 1)],
                [(4, 5), (2, 1), (3, 6)],
                [(2, 4), (1, 3), (6, 5)],
                [(3, 5), (2, 4), (1, 6)],
                [(2, 5), (4, 1), (3, 6)],
                [(5, 1), (6, 4), (3, 2)],
                [(4, 2), (5, 3), (1, 6)],
                [(1, 2), (4, 5), (6, 3)],
                [(2, 6), (1, 5), (4, 3)],
                [(6, 2), (3, 4), (5, 1)],
                [(5, 6), (3, 2), (1, 4)],
                [(5, 4), (6, 3), (2, 1)],
                [(5, 4), (1, 3), (6, 2)],
                [(3, 1), (5, 2), (6, 4)],
                [(2, 3), (6, 5), (1, 4)]
            ]
        else:
            expected_schedule = [
                [(6, 2), (5, 4), (3, 1)],
                [(5, 3), (2, 4), (1, 6)],
                [(1, 4), (6, 2), (5, 3)],
                [(6, 5), (1, 3), (4, 2)],
                [(1, 6), (3, 4), (5, 2)],
                [(1, 2), (5, 4), (3, 6)],
                [(2, 1), (6, 4), (3, 5)],
                [(4, 6), (5, 1), (3, 2)],
                [(5, 2), (3, 1), (4, 6)],
                [(2, 4), (5, 6), (1, 3)],
                [(5, 1), (2, 6), (3, 4)],
                [(6, 1), (2, 3), (4, 5)],
                [(4, 3), (2, 1), (6, 5)],
                [(3, 5), (6, 1), (4, 2)],
                [(1, 5), (2, 3), (6, 4)],
                [(1, 2), (6, 3), (4, 5)],
                [(2, 5), (4, 1), (6, 3)],
                [(1, 4), (3, 6), (2, 5)],
                [(3, 2), (4, 1), (5, 6)],
                [(1, 5), (2, 6), (4, 3)]
            ]
        schedule = scheduler.generate_schedule(try_once=True)
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for '
                              'quadruple round-robin competition'))
