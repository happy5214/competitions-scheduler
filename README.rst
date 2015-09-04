Generic schedulers for competitions
===================================

The goal of this package is to provide high-quality, randomized schedule
generators for competitions, particularly leagues. The schedulers generate
lists of rounds for competitions when provided a list of teams or a team count.

Right now, this library supports schedule generation for pure round-robin
competitions. While special wrappers are provided for round-robin leagues with
between 1 and 4 meetings between teams, competitions with more meetings
are possible.

Changes in v0.2.2
-----------------

- More tests

Changes in v0.2.1
-----------------

- Additional tests for higher-level round-robin schedules.

Changes in v0.2
---------------

- Standard round-robin schedulers for leagues with odd numbers of meetings.

.. image:: https://travis-ci.org/happy5214/competitions-scheduler.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.org/happy5214/competitions-scheduler
