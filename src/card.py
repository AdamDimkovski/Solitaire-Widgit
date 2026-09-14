# Card Class which holds Card Details

class Card:
    # The initializer/constructor method
    def __init__(self, suit, rank):
        self.suit = suit    
        self.rank = rank
        self.face_up = False

    def flip(self):
        self.face_up = True

    def image_filename(self):
        if self.face_up == False:
            return "assets//PNG//Cards//cardBack_red4.png"
        else:
            return f"assets//PNG//Cards//card{self.suit}{self.rank}.png"


    def __repr__(self):
        state = "up" if self.face_up else "down"
        return f"{self.rank} of {self.suit} ({state})"