# -*- coding: utf-8  -*-
"""Tests for round-robin schedulers."""

from __future__ import unicode_literals

from tests import TestCase

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
