# -*- coding: utf-8  -*-
"""Round-robin scheduling."""

from __future__ import print_function, unicode_literals

import copy
import random

from . import ScheduleGenerationFailed
from .scheduler import Scheduler


class RoundRobinScheduler(Scheduler):

    """A standard round-robin scheduler."""

    def __init__(self, teams):
        """Constructor.

        @param teams: A list of teams or the number of teams
        @type teams: list or int
        """
        if not isinstance(teams, list):
            teams = list(range(1, teams + 1))
        if len(teams) % 2 == 1:
            teams.append(None)
        self.teams = teams

    @property
    def match_count(self):
        """The number of matches per round."""
        return int(len(self.teams) / 2)

    def generate_round(self, matches):
        """Generate a round.

        @param matches: The generated matches
        @type matches: list
        @return: The generated round
        @rtype: list
        """
        round = []
        try:
            random.shuffle(matches)
            round.append(matches.pop(0))
            poss = copy.copy(matches)
            for __ in range(1, self.match_count):
                match = Scheduler.find_unique_match(round, poss)
                round.append(match)
                matches.remove(match)
            return round
        except IndexError:
            matches.extend(round)
            return None

    def generate_schedule(self, try_once=False):
        """Generate the schedule.

        @param try_once: Whether to only try once to generate a schedule
        @type try_once: bool
        @return: The generated schedule
        @rtype: list of lists of tuples
        @raise RuntimeError: Failed to create schedule within limits
        """
        rounds = []
        matches = self.generate_matches()

        for x in range(self.round_count):
            # print('Generating round %d' % (x + 1))
            for __ in range(10):
                next_round = self.generate_round(matches)
                if next_round:
                    rounds.append(next_round)
                    break
            else:
                # print('Error: Could not generate round. Restarting.')
                if not try_once:
                    return self.generate_schedule()
                else:
                    raise ScheduleGenerationFailed('Schedule generation failed.')

        return rounds


class DoubleRoundRobinScheduler(RoundRobinScheduler):

    """A standard double round-robin scheduler."""

    @property
    def round_count(self):
        """The number of rounds in a season."""
        return int((len(self.teams) - 1) * 2)

    def generate_matches(self):
        """Generate the matches for the season.

        @return: The matches to schedule
        @rtype: list
        """
        return [(team, opp)
                for team in self.teams
                for opp in self.teams
                if team != opp]


class QuadrupleRoundRobinScheduler(DoubleRoundRobinScheduler):

    """A standard quadruple round-robin scheduler."""

    @property
    def round_count(self):
        """The number of rounds in a season."""
        return int((len(self.teams) - 1) * 4)

    def generate_matches(self):
        """Generate the matches for the season.

        @return: The matches to schedule
        @rtype: list
        """
        return [(team, opp)
                for team in self.teams
                for opp in self.teams
                if team != opp] * 2
