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
          
        # Function to determine rules for moving card from pile a to b
        def tableau_check(self, card, column_index):
             
               # If destination is empty -> only king cards can be moved there
               if not self.tableau[column_index]:
                    
                    if card.rank == 13:
                         return True
                    else:
                         return False
               
               top_card = self.tableau[column_index][-1]
               
               colors_differ = (self.is_red(card) != self.is_red(top_card))
               
               ranks_fit = (card.rank == top_card.rank - 1)
               
               card_face_up = (top_card.face_up == True)
                         
               # Checks to see if destination card and input card are different colors
               if colors_differ and ranks_fit and card_face_up:
                    return True
               else:
                    return False
               
               
        # Function to determine rules for moving card from pile a to foundation
        def foundation_check(self, card, column_index):
             
             # If foundation pile is empty, only placing ace is allowed.
             if not self.foundations[column_index]:
               
                  if card.rank == 1:
                   return True
                  else:
                   return False
              
             top_card = self.foundations[column_index][-1]
             
             # Placing new card in existing pile -> suit must be same and rank must be greater by 1
             if(card.suit == top_card.suit and card.rank == top_card.rank + 1):
                  return True
             else:
                  return False
             
        # Function that handles selecting cards when moving
        def card_selection(self, source, source_pile_num, clicked_card_index):
             
             if(source == "Tableau"):
               column = self.tableau[source_pile_num]
               return column[clicked_card_index:]
                  
             if(source == "Waste"):
               return self.waste[-1:]
                  
             if(source == "Foundation"):
               pile = self.foundations[source_pile_num]
               return pile[-1:]
          
             # If source isn't any of the above, return nothing.
             return []
        
        # Function which handles moving cards between piles
        def card_moving(self, source, source_pile_num, clicked_card_index, destination_type, destination_pile_num):
          
          # Stores whatever cards are selected in list   
          cards_list = self.card_selection(source, source_pile_num, clicked_card_index)
          
          if not cards_list:
               return False
          
          if source_pile_num == destination_pile_num and source == destination_type:
               return False
          
          # The leading card of the selected cards
          leading_card = cards_list[0]
          
          # Checks to make sure all card moves are valid
          legal = False
          
          if(destination_type == "Tableau"):
               legal = self.tableau_check(leading_card, destination_pile_num)
                
          elif(destination_type == "Foundation" and len(cards_list) == 1):
               legal = self.foundation_check(leading_card, destination_pile_num)
          
          if not legal:
               return False
          
          # Handles Job 1
          if(source == "Tableau"):
               column = self.tableau[source_pile_num]
               del column[clicked_card_index:]

               # Handles Job 2
               if column and not column[-1].face_up:
                    column[-1].flip()
          
          elif(source == "Waste"):
               self.waste.pop()
               
          elif(source == "Foundation"):
               self.foundations[source_pile_num].pop()
               
          # Handles Job 3: legal moves will now map to where they should go instead of vanish
          if(destination_type == "Tableau"):
               self.tableau[destination_pile_num].extend(cards_list)
               
          elif(destination_type == "Foundation"):
               self.foundations[destination_pile_num].extend(cards_list)
          
          return True
            
        # Helper function which returns true if a card is heart or diamond       
        def is_red(self, card):
               
               if card.suit in {"Diamonds", "Hearts"}:
                    return True
               else:
                    return False
               
               
                    