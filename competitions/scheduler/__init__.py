# -*- coding: utf-8  -*-
"""Scheduler package."""

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


class ScheduleGenerationFailed(RuntimeError):

    """Exception for failed schedule generation.

    This is raised by implementations of Scheduler.generate_schedule() in the
    event that it cannot generate a schedule. This is usually because try_once
    was passed and the first attempt failed. The method will otherwise call
    itself until a schedule can be generated, and this will only fail if the
    recursion limit is reached, when a different error will be raised.
    """

    pass


class NoMatchFound(RuntimeError):

    """Exception for failure to find suitable match.

    This exception is meant for internal use. If this exception reaches
    consumers, there is a coding error and this exception should not be
    caught.
    """

    pass
