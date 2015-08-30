Generic schedulers for competitions
===================================

The goal of this package is to provide high-quality, randomized schedule
generators for competitions, particularly leagues. The schedulers generate
lists of rounds for competitions when provided a list of teams or a team count.

Right now, this library supports schedule generation for pure round-robin
competitions with even numbers of meetings. While special wrappers are provided
for double and quadruple round-robin leagues, competitions with more meetings
are possible. Be warned that these higher-level schedules are not tested.

.. image:: https://travis-ci.org/happy5214/competitions-scheduler.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.org/happy5214/competitions-scheduler
