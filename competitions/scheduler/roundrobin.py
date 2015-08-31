# -*- coding: utf-8  -*-
"""Round-robin scheduling."""

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

from __future__ import print_function, unicode_literals

import copy
import random

from . import NoMatchFound, ScheduleGenerationFailed
from .scheduler import Scheduler


class RoundRobinScheduler(Scheduler):

    """A standard round-robin scheduler."""

    def __init__(self, teams, meetings=0):
        """Constructor.

        @param teams: A list of teams or the number of teams
        @type teams: list or int
        @param meetings: The number of times teams meet each other
        @type meetings: int
        """
        if not isinstance(teams, list):
            teams = list(range(1, teams + 1))
        if len(teams) % 2 == 1:
            teams.append(None)
        self.teams = teams
        if meetings % 2 == 1:
            raise ValueError('Odd meeting numbers are not yet supported.')
        self.meetings = meetings

    @property
    def match_count(self):
        """The number of matches per round."""
        return int(len(self.teams) / 2)

    @property
    def round_count(self):
        """The number of rounds in a season."""
        return int((len(self.teams) - 1) * self.meetings)

    def generate_matches(self):
        """Generate the matches for the season.

        @return: The matches to schedule
        @rtype: list
        """
        is_odd = self.meetings % 2 == 1
        if is_odd:
            raise ValueError('Odd meeting numbers are not yet supported.')
            # evens = int((self.meetings - 1) / 2)
        else:
            evens = int(self.meetings / 2)

        # Even meetings
        matches = [(team, opp)
                   for team in self.teams
                   for opp in self.teams
                   if team != opp] * evens
        # TODO: Odd meetings
        return matches

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
        except NoMatchFound:
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

        for __ in range(self.round_count):
            for ___ in range(10):
                next_round = self.generate_round(matches)
                if next_round:
                    rounds.append(next_round)
                    break
            else:
                if not try_once:
                    return self.generate_schedule()
                else:
                    raise ScheduleGenerationFailed('Schedule generation failed.')

        return rounds


class DoubleRoundRobinScheduler(RoundRobinScheduler):

    """A standard double round-robin scheduler.

    This is an alias of RoundRobinScheduler, with meetings=2.
    """

    def __init__(self, teams):
        """Constructor.

        @param teams: A list of teams or the number of teams
        @type teams: list or int
        """
        super(DoubleRoundRobinScheduler, self).__init__(teams, meetings=2)


class QuadrupleRoundRobinScheduler(RoundRobinScheduler):

    """A standard quadruple round-robin scheduler.

    This is an alias of RoundRobinScheduler, with meetings=4.
    """

    def __init__(self, teams):
        """Constructor.

        @param teams: A list of teams or the number of teams
        @type teams: list or int
        """
        super(QuadrupleRoundRobinScheduler, self).__init__(teams, meetings=4)
