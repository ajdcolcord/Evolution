README - feeding

__init__.py - makes this folder into a Python package
constants.py - a container for constant values in evolution
dealerProxy.py - A proxy that parses input from dealer and calls player functions
diagram.txt - a top-level UML diagram of our classes
player.py - a player of evolution, including the feed method
playerTests.py - Contains unit tests for player.py
playerState.py - information necessary to a player (split to prevent cheating)
playerStateTests.py - Contains unit tests for playerState.py
species.py - representation of an evolution species
speciesTests.py - Contains unit tests for species.py
tests.py - Runs integration tests, comparing json input and output files
traitCard.py - a trait card with a name and food value

To use species.py, you'll want to use xattack in the containing folder. 
See that README for how to run it.
To use player.py, you'll want to use xfeed the same way.
To run tests, run python2.7 tests.py from command line.

To understand the code, we recommend you read through in the following order:
- diagram.txt
- playerState.py
- traitCard.py (since it's very short)
- species.py, the init and isAttackable functions
- player.py, especially the feed function
- dealerProxy.py
- tests.py
