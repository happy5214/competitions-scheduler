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

import itertools
import random
# import unittest

from . import TestCase, PY2, PY3

from competitions.scheduler import ScheduleGenerationFailed
from competitions.scheduler.roundrobin import (
    RoundRobinScheduler,
    SingleRoundRobinScheduler,
    DoubleRoundRobinScheduler,
    TripleRoundRobinScheduler,
    QuadrupleRoundRobinScheduler
)


class TestEvenRoundRobin(TestCase):

    """Tests for even-numbered round-robin scheduling."""

    def _test_match_generation(self, teams, multiplier=1):
        """Test even-numbered round-robin match generation (actual code)."""
        meetings = multiplier * 2
        scheduler = RoundRobinScheduler(teams, meetings=meetings)
        expected = list(itertools.permutations(scheduler.teams, 2)) * multiplier
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected, matches,
                              ('Incorrect matches generated for even-numbered '
                               'round-robin schedule with {} meetings for '
                               '{} teams.').format(meetings, teams))

    def test_match_generation(self):
        """Test even-numbered round-robin match generation."""
        for multiplier in range(1, 6):
            for teams in range(3, 21):
                self._test_match_generation(teams, multiplier)


class TestOddRoundRobin(TestCase):

    """Tests for odd-numbered round-robin scheduling."""

    def _test_matrix_generation(self, meetings, teams,
                                known_home_teams=None):
        """Test odd-numbered round-robin matrix generation."""
        scheduler = RoundRobinScheduler(teams, meetings=meetings)
        matrix = scheduler.generate_matrix(home_teams=known_home_teams)
        if known_home_teams:
            self.assertSequenceEqual(known_home_teams, scheduler.home_teams,
                                     'Home teams not stored.')
        home_teams = 0
        away_teams = 0
        odd_teams = teams % 2 == 1
        if odd_teams:
            teams += 1

        for x in range(teams):
            self.assertIsNone(matrix[x][x], 'Match against self not None.')
            opponents = matrix[x]
            home_count = opponents.count(True)
            away_count = opponents.count(False)
            if home_count > away_count:
                home_teams += 1
                if known_home_teams:
                    self.assertIn(scheduler.teams[x], known_home_teams,
                                  'Home team designation violated.')
                self.assertEqual(home_count, away_count + 1,
                                 'Team has too many home opponents.')
                if odd_teams and x != teams - 1:
                    self.assertTrue(opponents[-1],
                                    'Home excess not balanced by bye round.')
            else:
                away_teams += 1
                if known_home_teams:
                    self.assertNotIn(scheduler.teams[x], known_home_teams,
                                     'Away team designation violated.')
                self.assertEqual(away_count, home_count + 1,
                                 'Team has too many away opponents.')
                if odd_teams and x != teams - 1:
                    self.assertFalse(opponents[-1],
                                     'Away excess not balanced by bye round.')

        self.assertEqual(home_teams, away_teams,
                         'Home and away team counts not balanced.')

    def test_matrix_generation(self):
        """Test odd-numbered round-robin matrix generation."""
        team_counts = list(range(3, 21))
        meeting_counts = [1, 3, 5, 7, 9, 2, 4]
        for teams in team_counts:
            for meetings in meeting_counts:
                self._test_matrix_generation(meetings, teams)
                if teams > 8:
                    continue
                team_list = list(range(1, teams + 1))
                half = int(teams / 2)
                if teams % 2 == 1:
                    team_list.append(None)
                    half += 1
                for home_teams in itertools.permutations(team_list, half):
                    self._test_matrix_generation(meetings, teams, home_teams)


class TestRoundRobinWrappers(TestCase):

    """Tests to ensure that named RoundRobinScheduler wrappers are wrappers."""

    def test_wrappers(self):
        """Test that named RoundRobinScheduler wrappers are equivalent."""
        wrappers = [SingleRoundRobinScheduler, DoubleRoundRobinScheduler,
                    TripleRoundRobinScheduler, QuadrupleRoundRobinScheduler]
        for i in range(4):
            meetings = i + 1
            wrapper = wrappers[i]
            direct_scheduler = RoundRobinScheduler(4, meetings=meetings)
            wrapped_scheduler = wrapper(4)
            self.assertTrue(issubclass(wrapped_scheduler.__class__,
                                       direct_scheduler.__class__),
                            'Wrapper class is not a subclass of base class.')
            self.assertEqual(direct_scheduler.find_unique_match,
                             wrapped_scheduler.find_unique_match,
                             'find_unique_match different in base and wrapper.')
            self.assertEqual(direct_scheduler.matches_share_opponents,
                             wrapped_scheduler.matches_share_opponents,
                             ('matches_share_opponents different in base and '
                              'wrapper.'))
            self.assertEqual(direct_scheduler.generate_matches.__func__,
                             wrapped_scheduler.generate_matches.__func__,
                             'generate_matches different in base and wrapper.')
            self.assertEqual(direct_scheduler.generate_matrix.__func__,
                             wrapped_scheduler.generate_matrix.__func__,
                             'generate_matrix different in base and wrapper.')
            self.assertEqual(direct_scheduler.generate_round.__func__,
                             wrapped_scheduler.generate_round.__func__,
                             'generate_round different in base and wrapper.')
            self.assertEqual(direct_scheduler.generate_schedule.__func__,
                             wrapped_scheduler.generate_schedule.__func__,
                             'generate_schedule different in base and wrapper.')


class TestSingleRoundRobin(TestCase):

    """Tests for single round-robin scheduling."""

    def test_match_generation(self):
        """Test single round-robin match generation."""
        # Four teams
        random.seed(1)
        scheduler = SingleRoundRobinScheduler(4)
        if PY2:
            expected_matches = [
                (1, 2), (3, 1), (1, 4),
                (2, 3), (4, 2), (3, 4)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (4, 1),
                (2, 3), (2, 4), (3, 4)
            ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for single '
                               'round-robin schedule with four teams.'))
        # Three teams
        random.seed(1)
        scheduler = SingleRoundRobinScheduler(3)
        if PY2:
            expected_matches = [
                (2, 1), (1, 3), (3, 2),
                (1, None), (None, 2), (None, 3)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (2, 3),
                (1, None), (None, 2), (None, 3)
            ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for single '
                               'round-robin schedule with three teams.'))
        # Eight teams
        random.seed(1)
        scheduler = SingleRoundRobinScheduler(8)
        if PY2:
            expected_matches = [
                (1, 2), (3, 1), (4, 1), (1, 5), (6, 1), (1, 7), (1, 8),
                (2, 3), (2, 4), (5, 2), (6, 2), (7, 2), (2, 8),
                (4, 3), (5, 3), (3, 6), (3, 7), (3, 8),
                (5, 4), (4, 6), (4, 7), (8, 4),
                (6, 5), (7, 5), (5, 8),
                (7, 6), (8, 6),
                (8, 7)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (4, 1), (1, 5), (1, 6), (1, 7), (8, 1),
                (3, 2), (2, 4), (5, 2), (2, 6), (7, 2), (2, 8),
                (3, 4), (5, 3), (6, 3), (3, 7), (8, 3),
                (4, 5), (4, 6), (7, 4), (8, 4),
                (5, 6), (5, 7), (8, 5),
                (6, 7), (6, 8),
                (7, 8)
            ]
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for single '
                               'round-robin schedule with eight teams.'))

    def test_schedule_generation(self):
        """Test single round-robin schedule generation."""
        scheduler = SingleRoundRobinScheduler(8)
        # Failed attempt
        random.seed(17)
        self.assertRaises(ScheduleGenerationFailed,
                          scheduler.generate_schedule, try_once=True)
        # Successful attempt
        random.seed(4)
        if PY2:
            expected_schedule = [
                [(2, 5), (8, 6), (7, 1), (3, 4)],
                [(5, 8), (3, 7), (1, 2), (4, 6)],
                [(5, 4), (6, 3), (2, 7), (8, 1)],
                [(7, 8), (6, 5), (2, 4), (3, 1)],
                [(6, 2), (3, 8), (7, 5), (1, 4)],
                [(7, 6), (2, 3), (4, 8), (1, 5)],
                [(5, 3), (1, 6), (4, 7), (8, 2)]
            ]
        elif PY3:
            expected_schedule = [
                [(5, 7), (8, 4), (3, 6), (1, 2)],
                [(4, 2), (6, 8), (1, 5), (3, 7)],
                [(8, 1), (6, 4), (3, 5), (7, 2)],
                [(4, 1), (2, 3), (5, 8), (6, 7)],
                [(8, 3), (2, 6), (4, 5), (7, 1)],
                [(8, 2), (1, 3), (5, 6), (4, 7)],
                [(1, 6), (3, 4), (7, 8), (2, 5)]
            ]
        schedule = scheduler.generate_schedule(try_once=True)
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for '
                              'single round-robin competition'))

    def test_repeated_schedule_generation(self):
        """Test repeated single round-robin schedule generation."""
        scheduler = SingleRoundRobinScheduler(8)
        random.seed(17)
        if PY2:
            expected_schedule = [
                [(7, 5), (3, 6), (2, 1), (4, 8)],
                [(7, 3), (6, 5), (1, 8), (4, 2)],
                [(5, 3), (8, 6), (1, 4), (2, 7)],
                [(1, 6), (5, 2), (7, 8), (3, 4)],
                [(8, 5), (2, 3), (6, 4), (7, 1)],
                [(4, 7), (8, 3), (6, 2), (5, 1)],
                [(6, 7), (2, 8), (3, 1), (4, 5)]
            ]
        elif PY3:
            expected_schedule = [
                [(8, 7), (1, 6), (3, 5), (4, 2)],
                [(2, 6), (4, 3), (7, 1), (5, 8)],
                [(7, 3), (4, 1), (6, 8), (2, 5)],
                [(7, 4), (3, 1), (5, 6), (8, 2)],
                [(7, 2), (3, 6), (1, 5), (8, 4)],
                [(6, 4), (8, 3), (2, 1), (5, 7)],
                [(2, 3), (6, 7), (5, 4), (1, 8)]
            ]
        schedule = scheduler.generate_schedule()
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for repeated '
                              'single round-robin competition'))


class TestDoubleRoundRobin(TestCase):

    """Tests for double round-robin scheduling."""

    def test_schedule_generation(self):
        """Test double round-robin schedule generation."""
        scheduler = DoubleRoundRobinScheduler(8)
        # Failed attempt
        random.seed(5)
        self.assertRaises(ScheduleGenerationFailed,
                          scheduler.generate_schedule, try_once=True)
        # Successful attempt
        random.seed(2)
        if PY2:
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
        elif PY3:
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

    def test_repeated_schedule_generation(self):
        """Test repeated double round-robin schedule generation."""
        scheduler = DoubleRoundRobinScheduler(8)
        random.seed(5)
        if PY2:
            expected_schedule = [
                [(8, 4), (3, 7), (1, 6), (2, 5)],
                [(7, 1), (6, 4), (8, 2), (5, 3)],
                [(1, 8), (2, 4), (7, 6), (3, 5)],
                [(2, 6), (5, 7), (4, 3), (8, 1)],
                [(8, 5), (1, 3), (7, 4), (6, 2)],
                [(2, 7), (4, 8), (5, 1), (3, 6)],
                [(1, 7), (6, 5), (2, 8), (3, 4)],
                [(1, 4), (8, 3), (5, 2), (6, 7)],
                [(2, 3), (4, 1), (6, 8), (7, 5)],
                [(1, 2), (5, 8), (7, 3), (4, 6)],
                [(4, 2), (6, 3), (1, 5), (7, 8)],
                [(4, 5), (8, 7), (3, 2), (6, 1)],
                [(2, 1), (4, 7), (3, 8), (5, 6)],
                [(7, 2), (8, 6), (5, 4), (3, 1)]
            ]
        elif PY3:
            expected_schedule = [
                [(4, 3), (8, 2), (6, 7), (5, 1)],
                [(5, 6), (2, 4), (3, 8), (1, 7)],
                [(6, 5), (4, 8), (1, 3), (7, 2)],
                [(8, 4), (1, 2), (5, 3), (7, 6)],
                [(8, 5), (2, 3), (7, 1), (4, 6)],
                [(4, 5), (8, 6), (2, 7), (3, 1)],
                [(2, 8), (3, 5), (1, 6), (7, 4)],
                [(6, 2), (1, 8), (3, 4), (7, 5)],
                [(5, 4), (8, 7), (2, 1), (6, 3)],
                [(8, 1), (3, 6), (4, 7), (2, 5)],
                [(4, 1), (5, 2), (7, 3), (6, 8)],
                [(6, 4), (7, 8), (1, 5), (3, 2)],
                [(8, 3), (5, 7), (2, 6), (1, 4)],
                [(5, 8), (3, 7), (6, 1), (4, 2)]
            ]
        schedule = scheduler.generate_schedule()
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for repeated '
                              'double round-robin competition'))


class TestTripleRoundRobin(TestCase):

    """Tests for triple round-robin scheduling."""

    def test_match_generation(self):
        """Test triple round-robin match generation."""
        # Four teams
        random.seed(1)
        scheduler = TripleRoundRobinScheduler(4)
        if PY2:
            expected_matches = [
                (1, 2), (3, 1), (1, 4),
                (2, 3), (4, 2), (3, 4)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (4, 1),
                (2, 3), (2, 4), (3, 4)
            ]
        expected_matches.extend([
            (1, 2), (1, 3), (1, 4),
            (2, 1), (2, 3), (2, 4),
            (3, 1), (3, 2), (3, 4),
            (4, 1), (4, 2), (4, 3)
        ])
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for triple '
                               'round-robin schedule with four teams.'))
        # Three teams
        random.seed(1)
        scheduler = TripleRoundRobinScheduler(3)
        if PY2:
            expected_matches = [
                (2, 1), (1, 3), (3, 2),
                (1, None), (None, 2), (None, 3)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (2, 3),
                (1, None), (None, 2), (None, 3)
            ]
        expected_matches.extend([
            (1, 2), (1, 3), (1, None),
            (2, 1), (2, 3), (2, None),
            (3, 1), (3, 2), (3, None),
            (None, 1), (None, 2), (None, 3)
        ])
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for triple '
                               'round-robin schedule with three teams.'))
        # Eight teams
        random.seed(1)
        scheduler = TripleRoundRobinScheduler(8)
        if PY2:
            expected_matches = [
                (1, 2), (3, 1), (4, 1), (1, 5), (6, 1), (1, 7), (1, 8),
                (2, 3), (2, 4), (5, 2), (6, 2), (7, 2), (2, 8),
                (4, 3), (5, 3), (3, 6), (3, 7), (3, 8),
                (5, 4), (4, 6), (4, 7), (8, 4),
                (6, 5), (7, 5), (5, 8),
                (7, 6), (8, 6),
                (8, 7)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (4, 1), (1, 5), (1, 6), (1, 7), (8, 1),
                (3, 2), (2, 4), (5, 2), (2, 6), (7, 2), (2, 8),
                (3, 4), (5, 3), (6, 3), (3, 7), (8, 3),
                (4, 5), (4, 6), (7, 4), (8, 4),
                (5, 6), (5, 7), (8, 5),
                (6, 7), (6, 8),
                (7, 8)
            ]
        expected_matches.extend([
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 1), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
            (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
            (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8),
            (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8),
            (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8),
            (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8),
            (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7)
        ])
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for triple '
                               'round-robin schedule with eight teams.'))

    def test_schedule_generation(self):
        """Test triple round-robin schedule generation."""
        scheduler = TripleRoundRobinScheduler(8)
        # Failed attempt
        random.seed(12)
        self.assertRaises(ScheduleGenerationFailed,
                          scheduler.generate_schedule, try_once=True)
        # Successful attempt
        random.seed(1)
        if PY2:
            expected_schedule = [
                [(6, 5), (1, 7), (3, 4), (2, 8)],
                [(7, 5), (4, 3), (8, 6), (1, 2)],
                [(1, 8), (5, 3), (7, 2), (6, 4)],
                [(5, 8), (3, 1), (4, 6), (7, 2)],
                [(5, 4), (8, 6), (1, 2), (3, 7)],
                [(6, 7), (3, 8), (2, 5), (4, 1)],
                [(4, 3), (5, 1), (2, 7), (6, 8)],
                [(7, 4), (2, 3), (6, 5), (1, 8)],
                [(5, 8), (1, 3), (4, 7), (6, 2)],
                [(4, 5), (7, 6), (3, 8), (2, 1)],
                [(3, 5), (7, 1), (8, 2), (4, 6)],
                [(1, 4), (6, 3), (7, 5), (2, 8)],
                [(7, 8), (1, 5), (4, 2), (3, 6)],
                [(7, 3), (5, 2), (8, 4), (1, 6)],
                [(3, 7), (4, 8), (2, 6), (1, 5)],
                [(2, 4), (5, 7), (6, 1), (8, 3)],
                [(3, 2), (8, 5), (4, 1), (7, 6)],
                [(5, 4), (8, 7), (6, 1), (2, 3)],
                [(5, 3), (6, 2), (4, 7), (8, 1)],
                [(5, 6), (8, 7), (3, 1), (2, 4)],
                [(8, 4), (5, 2), (1, 7), (3, 6)]
            ]
        elif PY3:
            expected_schedule = [
                [(6, 5), (4, 3), (8, 1), (7, 2)],
                [(7, 4), (6, 2), (8, 5), (3, 1)],
                [(1, 5), (3, 2), (7, 4), (8, 6)],
                [(7, 8), (6, 4), (3, 5), (1, 2)],
                [(4, 7), (2, 8), (3, 1), (5, 6)],
                [(3, 6), (8, 7), (4, 5), (1, 2)],
                [(5, 7), (3, 4), (2, 6), (8, 1)],
                [(2, 4), (6, 3), (5, 7), (1, 8)],
                [(8, 2), (7, 1), (5, 3), (4, 6)],
                [(7, 3), (1, 5), (8, 4), (2, 6)],
                [(6, 8), (7, 2), (5, 4), (1, 3)],
                [(1, 7), (8, 5), (2, 3), (4, 6)],
                [(2, 7), (1, 6), (4, 5), (8, 3)],
                [(6, 7), (5, 2), (8, 3), (4, 1)],
                [(6, 3), (4, 8), (7, 5), (2, 1)],
                [(1, 4), (3, 7), (5, 6), (2, 8)],
                [(2, 4), (6, 1), (5, 8), (3, 7)],
                [(5, 3), (1, 6), (4, 2), (7, 8)],
                [(5, 2), (3, 4), (6, 8), (1, 7)],
                [(3, 2), (8, 4), (6, 7), (5, 1)],
                [(7, 6), (4, 1), (3, 8), (2, 5)]
            ]
        schedule = scheduler.generate_schedule(try_once=True)
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for '
                              'triple round-robin competition'))

    def test_repeated_schedule_generation(self):
        """Test repeated triple round-robin schedule generation."""
        scheduler = TripleRoundRobinScheduler(8)
        random.seed(12)
        if PY2:
            expected_schedule = [
                [(2, 3), (4, 1), (7, 5), (6, 8)],
                [(2, 1), (8, 7), (6, 3), (5, 4)],
                [(5, 6), (1, 7), (4, 8), (3, 2)],
                [(3, 5), (7, 6), (8, 2), (1, 4)],
                [(5, 7), (3, 6), (4, 2), (8, 1)],
                [(1, 5), (7, 3), (2, 8), (4, 6)],
                [(5, 8), (6, 1), (3, 4), (2, 7)],
                [(3, 6), (8, 4), (7, 1), (2, 5)],
                [(4, 5), (3, 8), (7, 1), (6, 2)],
                [(4, 3), (8, 6), (1, 5), (2, 7)],
                [(7, 6), (4, 2), (8, 3), (5, 1)],
                [(2, 6), (4, 7), (5, 3), (1, 8)],
                [(3, 2), (1, 6), (5, 8), (4, 7)],
                [(3, 7), (6, 1), (2, 4), (8, 5)],
                [(1, 3), (7, 4), (6, 5), (2, 8)],
                [(4, 3), (5, 7), (6, 2), (1, 8)],
                [(8, 3), (7, 2), (6, 5), (4, 1)],
                [(2, 1), (5, 3), (8, 4), (6, 7)],
                [(1, 3), (7, 8), (6, 4), (5, 2)],
                [(2, 5), (7, 8), (3, 1), (6, 4)],
                [(8, 6), (5, 4), (3, 7), (1, 2)]
            ]
        elif PY3:
            expected_schedule = [
                [(2, 5), (4, 1), (6, 7), (8, 3)],
                [(8, 4), (3, 6), (1, 5), (2, 7)],
                [(3, 2), (8, 5), (4, 1), (7, 6)],
                [(8, 1), (2, 5), (4, 6), (3, 7)],
                [(1, 7), (5, 3), (6, 8), (2, 4)],
                [(7, 2), (3, 6), (8, 1), (5, 4)],
                [(5, 7), (6, 2), (4, 3), (1, 8)],
                [(5, 8), (6, 1), (4, 7), (2, 3)],
                [(3, 1), (2, 4), (7, 8), (5, 6)],
                [(8, 4), (7, 1), (6, 2), (5, 3)],
                [(7, 3), (8, 5), (1, 6), (4, 2)],
                [(5, 6), (7, 4), (3, 1), (8, 2)],
                [(8, 2), (4, 7), (6, 3), (1, 5)],
                [(1, 7), (8, 6), (4, 5), (2, 3)],
                [(7, 8), (1, 4), (2, 6), (3, 5)],
                [(1, 3), (6, 4), (8, 7), (5, 2)],
                [(3, 8), (1, 2), (4, 6), (5, 7)],
                [(5, 1), (2, 8), (3, 4), (6, 7)],
                [(2, 1), (7, 5), (3, 4), (6, 8)],
                [(4, 5), (7, 2), (6, 1), (3, 8)],
                [(6, 5), (7, 3), (4, 8), (1, 2)]
            ]
        schedule = scheduler.generate_schedule()
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for repeated '
                              'triple round-robin competition'))


class TestQuadrupleRoundRobin(TestCase):

    """Tests for quadruple round-robin scheduling."""

    def test_schedule_generation(self):
        """Test quadruple round-robin schedule generation."""
        scheduler = QuadrupleRoundRobinScheduler(6)
        # Failed attempt
        random.seed(4)
        self.assertRaises(ScheduleGenerationFailed,
                          scheduler.generate_schedule, try_once=True)
        # Successful attempt
        random.seed(1)
        if PY2:
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
        elif PY3:
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

    def test_repeated_schedule_generation(self):
        """Test repeated quadruple round-robin schedule generation."""
        scheduler = QuadrupleRoundRobinScheduler(6)
        random.seed(4)
        if PY2:
            expected_schedule = [
                [(4, 1), (2, 6), (3, 5)],
                [(5, 2), (3, 6), (1, 4)],
                [(1, 5), (4, 6), (2, 3)],
                [(1, 3), (6, 5), (2, 4)],
                [(6, 2), (3, 4), (5, 1)],
                [(1, 2), (6, 3), (4, 5)],
                [(5, 2), (1, 6), (4, 3)],
                [(6, 1), (4, 2), (5, 3)],
                [(1, 3), (4, 5), (6, 2)],
                [(3, 2), (4, 6), (5, 1)],
                [(2, 6), (4, 3), (1, 5)],
                [(5, 6), (4, 1), (3, 2)],
                [(1, 4), (6, 5), (2, 3)],
                [(5, 6), (3, 1), (4, 2)],
                [(2, 1), (3, 6), (5, 4)],
                [(1, 6), (2, 4), (5, 3)],
                [(6, 3), (2, 1), (5, 4)],
                [(3, 4), (2, 5), (6, 1)],
                [(3, 5), (6, 4), (1, 2)],
                [(3, 1), (2, 5), (6, 4)]
            ]
        elif PY3:
            expected_schedule = [
                [(4, 6), (3, 2), (1, 5)],
                [(6, 2), (3, 4), (5, 1)],
                [(1, 4), (2, 5), (3, 6)],
                [(3, 1), (4, 2), (6, 5)],
                [(4, 1), (5, 2), (6, 3)],
                [(6, 1), (3, 5), (2, 4)],
                [(1, 3), (6, 2), (4, 5)],
                [(2, 5), (6, 4), (3, 1)],
                [(3, 4), (1, 2), (6, 5)],
                [(2, 3), (1, 6), (4, 5)],
                [(2, 4), (1, 3), (5, 6)],
                [(2, 1), (5, 4), (6, 3)],
                [(6, 4), (2, 1), (5, 3)],
                [(3, 2), (4, 6), (5, 1)],
                [(4, 1), (3, 6), (5, 2)],
                [(5, 6), (4, 3), (1, 2)],
                [(2, 3), (6, 1), (5, 4)],
                [(1, 5), (4, 3), (2, 6)],
                [(2, 6), (3, 5), (1, 4)],
                [(5, 3), (1, 6), (4, 2)]
            ]
        schedule = scheduler.generate_schedule()
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for repeated '
                              'quadruple round-robin competition'))


class TestQuintupleRoundRobin(TestCase):

    """Tests for quintuple round-robin scheduling."""

    def test_match_generation(self):
        """Test quintuple round-robin match generation."""
        # Four teams
        random.seed(1)
        scheduler = RoundRobinScheduler(4, meetings=5)
        if PY2:
            expected_matches = [
                (1, 2), (3, 1), (1, 4),
                (2, 3), (4, 2), (3, 4)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (4, 1),
                (2, 3), (2, 4), (3, 4)
            ]
        expected_matches.extend([
            (1, 2), (1, 3), (1, 4),
            (2, 1), (2, 3), (2, 4),
            (3, 1), (3, 2), (3, 4),
            (4, 1), (4, 2), (4, 3)
        ] * 2)
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for quintuple '
                               'round-robin schedule with four teams.'))
        # Three teams
        random.seed(1)
        scheduler = RoundRobinScheduler(3, meetings=5)
        if PY2:
            expected_matches = [
                (2, 1), (1, 3), (3, 2),
                (1, None), (None, 2), (None, 3)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (2, 3),
                (1, None), (None, 2), (None, 3)
            ]
        expected_matches.extend([
            (1, 2), (1, 3), (1, None),
            (2, 1), (2, 3), (2, None),
            (3, 1), (3, 2), (3, None),
            (None, 1), (None, 2), (None, 3)
        ] * 2)
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for quintuple '
                               'round-robin schedule with three teams.'))
        # Eight teams
        random.seed(1)
        scheduler = RoundRobinScheduler(8, meetings=5)
        if PY2:
            expected_matches = [
                (1, 2), (3, 1), (4, 1), (1, 5), (6, 1), (1, 7), (1, 8),
                (2, 3), (2, 4), (5, 2), (6, 2), (7, 2), (2, 8),
                (4, 3), (5, 3), (3, 6), (3, 7), (3, 8),
                (5, 4), (4, 6), (4, 7), (8, 4),
                (6, 5), (7, 5), (5, 8),
                (7, 6), (8, 6),
                (8, 7)
            ]
        elif PY3:
            expected_matches = [
                (1, 2), (3, 1), (4, 1), (1, 5), (1, 6), (1, 7), (8, 1),
                (3, 2), (2, 4), (5, 2), (2, 6), (7, 2), (2, 8),
                (3, 4), (5, 3), (6, 3), (3, 7), (8, 3),
                (4, 5), (4, 6), (7, 4), (8, 4),
                (5, 6), (5, 7), (8, 5),
                (6, 7), (6, 8),
                (7, 8)
            ]
        expected_matches.extend([
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 1), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
            (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
            (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8),
            (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8),
            (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8),
            (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8),
            (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7)
        ] * 2)
        matches = scheduler.generate_matches()
        self.assertCountEqual(expected_matches, matches,
                              ('Incorrect matches generated for quintuple '
                               'round-robin schedule with eight teams.'))

    def test_schedule_generation(self):
        """Test quintuple round-robin schedule generation."""
        scheduler = RoundRobinScheduler(6, meetings=5)
        # Failed attempt
        random.seed(8)
        self.assertRaises(ScheduleGenerationFailed,
                          scheduler.generate_schedule, try_once=True)
        # Successful attempt
        random.seed(1)
        if PY2:
            expected_schedule = [
                [(5, 2), (4, 1), (3, 6)],
                [(2, 1), (4, 3), (5, 6)],
                [(2, 5), (6, 3), (1, 4)],
                [(3, 5), (6, 4), (2, 1)],
                [(3, 6), (4, 1), (2, 5)],
                [(4, 2), (3, 1), (6, 5)],
                [(3, 4), (5, 6), (2, 1)],
                [(3, 5), (2, 6), (4, 1)],
                [(6, 3), (2, 4), (5, 1)],
                [(3, 2), (5, 1), (6, 4)],
                [(1, 6), (5, 4), (2, 3)],
                [(5, 3), (2, 6), (1, 4)],
                [(4, 3), (1, 2), (5, 6)],
                [(6, 1), (2, 3), (4, 5)],
                [(3, 6), (4, 2), (1, 5)],
                [(5, 2), (1, 6), (3, 4)],
                [(4, 6), (3, 1), (2, 5)],
                [(6, 2), (5, 4), (1, 3)],
                [(6, 2), (1, 3), (4, 5)],
                [(1, 5), (4, 3), (6, 2)],
                [(5, 3), (6, 1), (2, 4)],
                [(3, 2), (1, 6), (5, 4)],
                [(1, 5), (3, 2), (6, 4)],
                [(5, 3), (1, 2), (4, 6)],
                [(1, 3), (4, 2), (6, 5)]
            ]
        elif PY3:
            expected_schedule = [
                [(4, 6), (2, 5), (3, 1)],
                [(3, 4), (2, 5), (6, 1)],
                [(5, 1), (4, 3), (2, 6)],
                [(3, 6), (4, 5), (2, 1)],
                [(6, 4), (5, 3), (2, 1)],
                [(2, 4), (1, 3), (5, 6)],
                [(2, 3), (4, 1), (6, 5)],
                [(2, 5), (1, 4), (6, 3)],
                [(6, 4), (2, 3), (5, 1)],
                [(3, 1), (4, 2), (6, 5)],
                [(6, 1), (4, 5), (3, 2)],
                [(3, 2), (1, 5), (4, 6)],
                [(6, 2), (1, 4), (5, 3)],
                [(6, 1), (4, 3), (5, 2)],
                [(5, 4), (1, 2), (6, 3)],
                [(4, 6), (3, 2), (5, 1)],
                [(5, 6), (3, 4), (1, 2)],
                [(2, 4), (6, 3), (1, 5)],
                [(1, 6), (3, 4), (5, 2)],
                [(6, 2), (1, 4), (3, 5)],
                [(2, 4), (1, 6), (5, 3)],
                [(5, 4), (1, 3), (2, 6)],
                [(1, 2), (3, 6), (4, 5)],
                [(3, 5), (2, 6), (4, 1)],
                [(4, 2), (1, 3), (5, 6)]
            ]
        schedule = scheduler.generate_schedule(try_once=True)
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for '
                              'quintuple round-robin competition'))


class TestSextupleRoundRobin(TestCase):

    """Tests for sextuple round-robin scheduling."""

    def test_schedule_generation(self):
        """Test sextuple round-robin schedule generation."""
        scheduler = RoundRobinScheduler(6, meetings=6)
        # Failed attempt
        random.seed(35)
        self.assertRaises(ScheduleGenerationFailed,
                          scheduler.generate_schedule, try_once=True)
        # Successful attempt
        random.seed(1)
        if PY2:
            expected_schedule = [
                [(6, 4), (3, 1), (2, 5)],
                [(3, 1), (6, 5), (4, 2)],
                [(6, 1), (2, 3), (5, 4)],
                [(5, 1), (2, 6), (3, 4)],
                [(1, 6), (2, 5), (3, 4)],
                [(5, 6), (4, 3), (2, 1)],
                [(2, 6), (3, 5), (4, 1)],
                [(3, 1), (2, 5), (4, 6)],
                [(1, 4), (3, 5), (6, 2)],
                [(1, 2), (5, 4), (6, 3)],
                [(5, 2), (6, 4), (1, 3)],
                [(1, 3), (4, 2), (6, 5)],
                [(5, 3), (2, 6), (4, 1)],
                [(5, 1), (4, 6), (3, 2)],
                [(3, 2), (1, 6), (4, 5)],
                [(1, 3), (4, 6), (5, 2)],
                [(3, 6), (4, 5), (2, 1)],
                [(2, 3), (4, 5), (1, 6)],
                [(1, 2), (5, 3), (6, 4)],
                [(4, 1), (3, 2), (6, 5)],
                [(1, 4), (6, 3), (5, 2)],
                [(1, 5), (3, 6), (4, 2)],
                [(5, 1), (2, 4), (6, 3)],
                [(1, 2), (3, 6), (5, 4)],
                [(5, 6), (1, 4), (2, 3)],
                [(5, 3), (6, 1), (2, 4)],
                [(4, 3), (1, 5), (6, 2)],
                [(2, 1), (3, 4), (5, 6)],
                [(6, 1), (2, 4), (3, 5)],
                [(1, 5), (6, 2), (4, 3)]
            ]
        elif PY3:
            expected_schedule = [
                [(6, 4), (2, 3), (5, 1)],
                [(4, 5), (1, 2), (3, 6)],
                [(3, 4), (1, 2), (6, 5)],
                [(2, 6), (5, 3), (4, 1)],
                [(6, 3), (1, 5), (2, 4)],
                [(5, 6), (3, 2), (1, 4)],
                [(6, 1), (4, 2), (5, 3)],
                [(1, 3), (6, 4), (5, 2)],
                [(5, 1), (3, 4), (6, 2)],
                [(4, 1), (5, 6), (3, 2)],
                [(4, 5), (6, 1), (2, 3)],
                [(2, 1), (5, 4), (3, 6)],
                [(6, 2), (4, 5), (3, 1)],
                [(1, 5), (2, 4), (3, 6)],
                [(2, 6), (1, 5), (4, 3)],
                [(4, 6), (2, 1), (5, 3)],
                [(3, 1), (2, 5), (6, 4)],
                [(1, 6), (4, 2), (3, 5)],
                [(6, 1), (2, 3), (5, 4)],
                [(1, 4), (6, 2), (3, 5)],
                [(5, 2), (1, 4), (6, 3)],
                [(5, 6), (2, 4), (3, 1)],
                [(3, 4), (6, 5), (1, 2)],
                [(2, 5), (4, 1), (6, 3)],
                [(4, 3), (5, 1), (2, 6)],
                [(2, 5), (4, 6), (1, 3)],
                [(1, 3), (5, 2), (4, 6)],
                [(1, 6), (5, 4), (3, 2)],
                [(2, 1), (4, 3), (6, 5)],
                [(3, 5), (1, 6), (4, 2)]
            ]
        schedule = scheduler.generate_schedule(try_once=True)
        self.assertListEqual(expected_schedule, schedule,
                             ('Wrong schedule created for '
                              'sextuple round-robin competition'))
