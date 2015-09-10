Generic schedulers for competitions
===================================

The goal of this package is to provide high-quality, randomized schedule
generators for competitions, particularly leagues. The schedulers generate
lists of rounds for competitions when provided a list of teams or a team count.

Right now, this library supports schedule generation for pure round-robin
competitions. While special wrappers are provided for round-robin leagues with
between 1 and 4 meetings between teams, competitions with more meetings
are possible.

There will be a v0.3, but I don't know what should be in it. Should I clone
scheduling formulas from real sports leagues? Do you want knockout cups, playoffs,
or more predictable round-robin scheduling? I won't know unless you tell me.
Open feature requests on this project's GitHub repo and tell me what you want to
see in version 0.3!

Changes in v0.2.4
-----------------

- Reorganized and re-implemented several tests. 

Changes in v0.2.2 and v0.2.3
----------------------------

- More tests.

Changes in v0.2.1
-----------------

- Additional tests for higher-level round-robin schedules.

Changes in v0.2
---------------

- Standard round-robin schedulers for leagues with odd numbers of meetings.

.. image:: https://travis-ci.org/happy5214/competitions-scheduler.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.org/happy5214/competitions-scheduler
