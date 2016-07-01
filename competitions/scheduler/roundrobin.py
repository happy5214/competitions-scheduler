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

    def _generate_home_teams(self, home_teams=None):
        """Generate the list of home teams for a matrix."""
        team_count = len(self.teams)  # Number of teams
        odd_team_count = None in self.teams  # Whether there is a blank placeholder

        if not home_teams:  # Randomly select home teams
            if odd_team_count:
                home_count = (team_count - 1) // 2
                homes = random.sample(range(team_count - 1), home_count)
                homes.append(team_count - 1)  # Spacer is always home
            else:
                home_count = team_count // 2
                homes = random.sample(range(team_count), home_count)
            self._home_teams = [self.teams[i] for i in homes]
        else:  # if home_teams. Use provided teams.
            self._home_teams = home_teams
            homes = [self.teams.index(home) for home in home_teams]

        return homes

    def generate_matrix(self, home_teams=None):
        """Generate a schedule matrix for odd meeting counts."""
        team_count = len(self.teams)  # Number of teams
        home_at_home = team_count // 2  # "Home" teams have ceiling(half) of their matches at home
        away_at_home = (team_count - 1) // 2  # "Away" teams have floor(half) at home
        odd_team_count = None in self.teams  # Whether there is a blank placeholder
        homes = self._generate_home_teams(home_teams)
        matrix = [[None] * team_count for __ in range(team_count)]
        for i in range(team_count - 1):
            home_team = i in homes  # Whether the team is a home team
            home_count = (away_at_home
                          if not home_team or odd_team_count else home_at_home)
            home_count -= matrix[i].count(True)  # Check previously assigned match pairings
            try:
                if odd_team_count:
                    home_opps = random.sample(list(range(i + 1, team_count - 1)),
                                              home_count)
                    if home_team:
                        home_opps.append(team_count - 1)
                else:
                    home_opps = random.sample(list(range(i + 1, team_count)),
                                              home_count)
                for opp in range(i + 1, team_count):
                    is_home = opp in home_opps
                    matrix[i][opp] = is_home
                    matrix[opp][i] = not is_home
            except ValueError:  # Recurse
                return self.generate_matrix(home_teams=home_teams)
        return matrix

    def _generate_even_matches(self, evens):
        """Generate a list of matches for even meeting counts."""
        return [(team, opp)
                for team in self.teams
                for opp in self.teams
                if team != opp] * evens

    def _generate_odd_matches(self, home_teams=None):
        """Generate a list of matches for odd meeting counts."""
        matrix = self.generate_matrix(home_teams=home_teams)
        matches = []
        for team_idx in range(len(self.teams)):
            for opp_idx in range(team_idx + 1, len(self.teams)):
                if matrix[team_idx][opp_idx]:
                    matches.append((self.teams[team_idx],
                                    self.teams[opp_idx]))
                else:
                    matches.append((self.teams[opp_idx],
                                    self.teams[team_idx]))
        return matches

    def generate_matches(self, home_teams=None):
        """Generate the matches for the season.

        @return: The matches to schedule
        @rtype: list
        """
        is_odd = self.meetings % 2 == 1
        evens = self.meetings // 2

        matches = self._generate_even_matches(evens) if evens > 0 else []
        if is_odd:
            matches.extend(self._generate_odd_matches(home_teams))

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

    def _generate_schedule_round(self, matches):
        """Fully generate a round for a schedule."""
        for ___ in range(10):
            next_round = self.generate_round(matches)
            if next_round:
                return next_round
        else:
            raise ScheduleGenerationFailed('Schedule generation failed.')

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

        try:
            for __ in range(self.round_count):
                rounds.append(self._generate_schedule_round(matches))
        except ScheduleGenerationFailed as ex:
            if try_once:
                raise ex
            else:
                return self.generate_schedule(try_once, home_teams)

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
