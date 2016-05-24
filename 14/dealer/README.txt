README - dealer

dealer.py - Contains methods necessary for running the Evolution game.
dealerTests.py - Contains tests for dealer.py methods.

feedAction.py - Contains the Abstract class with a factory method for a feeding action from a player's response.
  noFeedAction.py - runs feed methods for a feeding action of False
  vegFeedAction.py - runs feed methods for feeding a vegetarian Species
  fatStoreAction.py - runs feed methods for storing fat tokens on a Species
  carnFeedAction.py - runs feeding and attacking methods for one Species attacking another Species
feedActionTests.py - Contains tests for feedAction.py and subclasses

playerAction.py - Contains object representation responsible for performing all actions for one player
    boardTrade.py - Contains object representation responsible for trading for a new species
    replaceTrait.py - Contains object representation responsible for replacing a trait on a species
    growBody.py - Contains object representation responsible for growing a body size on a species
    growPopulation.py - Contains object representation responsible for growing a population size on a species
playerActionTests.py - Contains unit tests for each action type

proxyPlayer.py - Contains a proxy to send, receive, and parse date for external players

To run unit tests for dealer.py, run the command "python dealerTests.py".
To run unit tests for feedAction.py (and subclasses), run the command "python feedActionTests.py".

To understand the code in dealer.py, first understand the data representation 
for the dealer class in the __init__ function. The dealer uses other 
representations for Players, Species, TraitCards, and PlayerStates. See README
in feeding directory for details on those classes. feedAction objects are created
each time the request_feed method (in dealer) is called.
