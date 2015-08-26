"""Double round-robin scheduling."""

import copy
import random

from scheduler import Scheduler


class DoubleRoundRobinScheduler(Scheduler):

    """A standard double round-robin scheduler."""

    @staticmethod
    def generate_matches(teams):
        """Generate the matches for the season.

        @param teams: The teams to generate matches for
        @type teams: list or int
        @return: The matches to schedule
        @rtype: list
        """
        if not isinstance(teams, list):
            teams = range(1, teams + 1)
        opps = {}
        for team in teams:
            opponents = []
            for opp in teams:
                if team != opp:
                    opponents.append(opp)
            opps[team] = opponents
        matches = []
        for team in teams:
            for opp in opps[team]:
                matches.append((team,opp))
        return matches

    @staticmethod
    def generate_round(match_num, matches):
        """Generate a round.

        @param match_num: Number of matches per round
        @type match_num: int
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
            for x in range(1, match_num):
                match = Scheduler.find_unique_match(round, poss)
                round.append(match)
                matches.remove(match)
            return round
        except IndexError:
            matches.extend(round)
            return None

    @staticmethod
    def generate_schedule(teams, try_once=False):
        """Generate the schedule.

        @param teams: A list of teams or the number of teams
        @type teams: list or int
        @param try_once: Whether to only try once to generate a schedule
        @type try_once: bool
        @return: The generated schedule
        @rtype: list of lists of tuples
        @raise RuntimeError: Failed to create schedule within limits
        """
        match_count = 0
        round_count = 0
        rounds = []
        if type(teams) != list:
            match_count = teams / 2
            round_count = (teams - 1) * 2
        else:
            match_count = len(teams) / 2
            round_count = (len(teams) - 1) * 2
        matches = DoubleRoundRobinScheduler.generate_matches(teams)

        for x in range(round_count):
            print 'Generating round %d' % (x + 1)
            for i in range(10):
                next_round = DoubleRoundRobinScheduler.generate_round(match_count,
                                                                      matches)
                if next_round:
                    rounds.append(next_round)
                    break
            else:
                print 'Error: Could not generate round. Restarting.'
                if not try_once:
                    return DoubleRoundRobinScheduler.generate_schedule(teams)
                else:
                    raise RuntimeError('Schedule generation failed.')

        return rounds
