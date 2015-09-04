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
        self.meetings = meetings

    @property
    def match_count(self):
        """The number of matches per round."""
        return int(len(self.teams) / 2)

    @property
    def round_count(self):
        """The number of rounds in a season."""
        return int((len(self.teams) - 1) * self.meetings)

    @property
    def home_teams(self):
        """The "home" teams from the previous schedule generation."""
        if hasattr(self, '_home_teams'):
            return tuple(self._home_teams)
        else:
            return ()

    def generate_matrix(self, home_teams=None):
        """Generate a schedule matrix for odd meeting counts."""
        team_count = len(self.teams)
        odd_team_count = None in self.teams
        if not home_teams:
            if odd_team_count:
                home_count = int((team_count - 1) / 2)
                homes = random.sample(range(team_count - 1), home_count)
                homes.append(team_count - 1)
            else:
                home_count = int(team_count / 2)
                homes = random.sample(range(team_count), home_count)
            self._home_teams = [self.teams[i] for i in homes]
        else:
            self._home_teams = home_teams
            homes = [self.teams.index(home) for home in home_teams]
        home_per_home = int(team_count / 2)
        home_per_away = int((team_count - 1) / 2)
        matrix = [[None] * team_count for __ in range(team_count)]
        for i in range(team_count - 1):
            home_team = i in homes
            home_count = (home_per_away
                          if not home_team or odd_team_count else home_per_home)
            for x in range(i):
                if matrix[i][x]:
                    home_count -= 1
            try:
                if odd_team_count:
                    home_opps = random.sample([x for x in range(i + 1,
                                                                team_count - 1)],
                                              home_count)
                    if home_team:
                        home_opps.append(team_count - 1)
                else:
                    home_opps = random.sample([x for x in range(i + 1,
                                                                team_count)],
                                              home_count)
                for opp in range(i + 1, team_count):
                    if opp in home_opps:
                        matrix[i][opp] = True
                        matrix[opp][i] = False
                    else:
                        matrix[i][opp] = False
                        matrix[opp][i] = True
            except ValueError:
                return self.generate_matrix(home_teams=home_teams)
        return matrix

    def generate_matches(self, home_teams=None):
        """Generate the matches for the season.

        @return: The matches to schedule
        @rtype: list
        """
        is_odd = self.meetings % 2 == 1
        if is_odd:
            evens = int((self.meetings - 1) / 2)
        else:
            evens = int(self.meetings / 2)

        # Even meetings
        if evens > 0:
            matches = [(team, opp)
                       for team in self.teams
                       for opp in self.teams
                       if team != opp] * evens
        else:
            matches = []
        # TODO: Odd meetings
        if is_odd:
            matrix = self.generate_matrix(home_teams=home_teams)
            odd_matches = []
            for team_idx in range(len(self.teams)):
                for opp_idx in range(team_idx + 1, len(self.teams)):
                    if matrix[team_idx][opp_idx]:
                        odd_matches.append((self.teams[team_idx],
                                            self.teams[opp_idx]))
                    else:
                        odd_matches.append((self.teams[opp_idx],
                                            self.teams[team_idx]))
            matches.extend(odd_matches)
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

    def generate_schedule(self, try_once=False, home_teams=None):
        """Generate the schedule.

        @param try_once: Whether to only try once to generate a schedule
        @type try_once: bool
        @return: The generated schedule
        @rtype: list of lists of tuples
        @raise RuntimeError: Failed to create schedule within limits
        """
        rounds = []
        matches = self.generate_matches(home_teams=home_teams)

        for __ in range(self.round_count):
            for ___ in range(10):
                next_round = self.generate_round(matches)
                if next_round:
                    rounds.append(next_round)
                    break
            else:
                if not try_once:
                    return self.generate_schedule(home_teams=home_teams)
                else:
                    raise ScheduleGenerationFailed('Schedule generation failed.')

        return rounds


# Aliases for common meeting counts
class SingleRoundRobinScheduler(RoundRobinScheduler):

    """A standard single round-robin scheduler.

    This is an alias of RoundRobinScheduler, with meetings=1.
    """

    def __init__(self, teams):
        """Constructor.

        @param teams: A list of teams or the number of teams
        @type teams: list or int
        """
        super(SingleRoundRobinScheduler, self).__init__(teams, meetings=1)


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


class TripleRoundRobinScheduler(RoundRobinScheduler):

    """A standard triple round-robin scheduler.

    This is an alias of RoundRobinScheduler, with meetings=3.
    """

    def __init__(self, teams):
        """Constructor.

        @param teams: A list of teams or the number of teams
        @type teams: list or int
        """
        super(TripleRoundRobinScheduler, self).__init__(teams, meetings=3)


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
