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

            # Will hold waste pile cards
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

        # Generates full deck of cards before game
        def create_full_deck(self):
             deck = []
             for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
                  for rank in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
                        deck.append(Card(suit, rank))

             return deck
        
        
        # Deals tableau piles at start of game
        @staticmethod
        def deal_to_tableau(deck):
             
             tableau = []
             
             # 7 tabelau Piles
             for column_index in range(7):
                  
                  # Each tableau stack
                  this_column = []
                  numcards_in_column = column_index + 1

                  for i in range(numcards_in_column):
                       card = deck.pop()
                       this_column.append(card)

                  this_column[-1].flip()
                  tableau.append(this_column)

             stock = deck
             return tableau, stock

        # Function to select next card from stock onto waste
        def stock_to_waste(self):
             
               # If neither pile is populated yet (before new game)
               if not self.waste and not self.stock:
                    return None
             
               # If stock stack is empty
               if not self.stock:
                    
                    # Well theres nothing in stock pile, reappend everything to the stock from waste, in direct order
                    while self.waste:
                         
                         # Appends popped waste card to card variable
                         card = self.waste.pop()
                         
                         # Flips over card again
                         card.flip()
                         
                         # Appends now flipped card back into stock pile.
                         self.stock.append(card)
                         
               # Store popped card
               card = self.stock.pop()
               
               # Flip card before appending
               card.flip()
               
               # Append card to waste
               self.waste.append(card)
               
               return card
            

             
                       
