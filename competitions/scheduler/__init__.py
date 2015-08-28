"""Scheduler package."""

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
