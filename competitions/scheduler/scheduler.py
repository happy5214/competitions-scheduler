"""Base class code for schedulers."""


class Scheduler(object):

    """Base class for schedulers.

    This class includes general-purpose scheduler functionality.
    """

    @staticmethod
    def matches_share_opponents(match1, match2):
        """Check matches for shared opponents.

        @param match1: The first match
        @type match1: tuple
        @param match2: The second match
        @type match2: tuple
        @return: Whether the first and second matches share an opponent
        @rtype: bool
        """
        (match1_1, match1_2) = match1
        return (match1_1 in match2 or match1_2 in match2)

    @staticmethod
    def find_unique_match(matches, rest):
        """Find a unique match.

        @param matches: The matches to check against
        @type matches: list
        @param rest: The matches to check for a unique match
        @type rest: list
        @return: The first unique match found
        @rtype: tuple
        @raise IndexError: If no unique match is found
        """
        while True:
            possibility = rest.pop(0)
            for match in matches:
                if Scheduler.matches_share_opponents(match, possibility):
                    possibility = None
                    break
            if possibility:
                return possibility

    @staticmethod
    def generate_schedule(teams, try_once=False):
        """Generate the schedule.

        This method must be overridden by subclasses.

        @param teams: A list of teams or the number of teams
        @type teams: list or int
        @param try_once: Whether to only try once to generate a schedule
        @type try_once: bool
        @return: The generated schedule
        @rtype: list of lists of tuples
        """
        raise NotImplementedError
