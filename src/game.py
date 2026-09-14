# Game Class which holds Game Details
import random

from card import Card

class Game:
        # The initializer/constructor method
        def __init__(self):

            # Will hold Card Objects
            self.deck = []

            # Will hold 7 list of Card
            self.tableau = []

            # Will hold 4 lists of Cards
            self.foundations = []

            # Will hold stock pile cards
            self.stock = []

            # Will hol waste pile cards
            self.waste = []

        def new_game(self):
              
            # Build a deck
            deck = self.create_full_deck()
            random.shuffle(deck)

            # Sepertes all the cards between the 7 piles and stock pile
            self.tableau, self.stock = self.deal_to_tableau(deck)

            # Generate 4 foundation piles (list)
            self.foundations = [[], [], [], []]

            # Generate 1 list for waste cards
            self.waste = []

        def create_full_deck(self):
             deck = []
             for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
                  for rank in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
                        deck.append(Card(suit, rank))

             return deck

        def deal_to_tableau(self, deck):
             for column_index in range(7):
                  this_column = []
                  numcards_in_column = column_index + 1

                  for i in range(numcards_in_column):
                       card = deck.pop()
                       this_column.append(card)

                  this_column[-1].flip()
                  self.tableau.append(this_column)

             stock = deck
             return self.tableau, stock


             
                       
