# -*- coding: utf-8  -*-
"""Base class code for schedulers."""

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

from . import NoMatchFound


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
        @raise NoMatchFound: If no unique match is found
        """
        while True:  # This will exit with the return statement or an error.
            try:
                possibility = rest.pop(0)  # Possibly unique match
                for match in matches:
                    if Scheduler.matches_share_opponents(match, possibility):
                        possibility = None  # Match is not unique.
                        break  # Try again.
                if possibility:  # No more matches to compare against.
                    return possibility  # This match is unique.
            except IndexError:  # We've run out of possibilities.
                raise NoMatchFound  # Raise exception to caller

    def generate_schedule(self, try_once=False):
        """Generate the schedule.

        This method must be overridden by subclasses.

        @param try_once: Whether to only try once to generate a schedule
        @type try_once: bool
        @return: The generated schedule
        @rtype: list of lists of tuples
        """
        raise NotImplementedError
