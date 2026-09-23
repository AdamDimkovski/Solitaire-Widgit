import tkinter as tk

from PIL import Image, ImageTk

class AppWindow:
    def __init__(self, root, game, click_callback):
        self.root = root
        self.root.title("Solitaire")
        self.root.geometry("1000x1000")
        self.root.resizable(False, False)
        self.game = game 
        
        # Card Highlighting Variables
        self.selected_card = None
        self.canvas_ID = None
        self.card_positions = []
        self.card_images = []
        
        # Stock/Waste Pile Variables
        self.stock_x = 900
        self.stock_y = 100
        self.waste_x = 750
        self.waste_y = 100
        
        # Save the callback function passed from main.py
        self.click_callback = click_callback

        # Tag which holds my background image
        self.bg_image = tk.PhotoImage(
            file="assets//Background//backgroundImage.png"
        )

        # Adds placeholder image for foundation cards and resizes them
        self.ace_image = self.load_and_resize("assets//PNG//Cards//cardPlaceholder.png")

        # Adds drawpile image for drawpile and resizes it
        self.drawpile_image = self.load_and_resize("assets//PNG//Cards//cardBack_red4.png")

        # Create and place widgets
        self.create_widgets()
        
        self.refresh_board()
        
        
        
    # Function that creates UI widgits
    def create_widgets(self):

        # Create the game canvas
        self.canvas = tk.Canvas(
            self.root,
            width=1000,
            height=1000,
            highlightthickness=0
        )

        self.canvas.place(x=0, y=0)

        # Put background onto Canvas
        self.canvas.create_image(
            0,
            0,
            image=self.bg_image,
            anchor="nw"
        )

        # Put foundation placeholders on top of background
        # Foundation Card 1
        self.canvas.create_image(
            250,
            100,
            image=self.ace_image
        )

        # Foundation Card 2
        self.canvas.create_image(
            375,
            100,
            image=self.ace_image
        )

        # Foundation Card 3
        self.canvas.create_image(
            500,
            100,
            image=self.ace_image
        )

        # Foundation Card 4
        self.canvas.create_image(
            625,
            100,
            image=self.ace_image
        )

        # New Game button
        self.button = tk.Button(
            self.root,
            text="New Game",
            command=self.click_callback,
            font=("Arial", 16, "bold"),
            bg="#222222",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            relief="flat",
            bd=0,
            width=12,
            height=2
        )

        self.button.place(x=15, y=15)

        # Undo Button
        self.button = tk.Button(
            self.root,
            text="Undo Move",
            command=self.click_callback,
            font=("Arial", 16, "bold"),
            bg="#222222",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            relief="flat",
            bd=0,
            width=12,
            height=2
        )

        self.button.place(x=15, y=115)

        # Place Lowerpile placeholders
        # Lowerpile 1
        self.canvas.create_image(
            125,
            300,
            image=self.ace_image
        )
        
        # Lowerpile 2
        self.canvas.create_image(
            250,
            300,
            image=self.ace_image
        )

        # Lowerpile 3
        self.canvas.create_image(
            375,
            300,
            image=self.ace_image
        )
        
        # Lowerpile 4
        self.canvas.create_image(
            500,
            300,
            image=self.ace_image
        )

        # Lowerpile 5
        self.canvas.create_image(
            625,
            300,
            image=self.ace_image
        )
                
        # Lowerpile 6
        self.canvas.create_image(
            750,
            300,
            image=self.ace_image
        )

        # Lowerpile 7
        self.canvas.create_image(
            875,
            300,
            image=self.ace_image
        )
        
            
        # Card Click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    # Function to refresh cards on screen
    def refresh_board(self):

        # Clear previous render
        self.canvas.delete("card")
        self.card_images = []
        
        self.card_positions = []
        
        # Handles reseting selected cards if game restarts
        self.selected_card = None

        if self.canvas_ID is not None:
            self.canvas.delete(self.canvas_ID)

        self.canvas_ID = None

        # Draw tableau columns
        tableau_start_x = 125 # The First Tableau Pile X Position
        tableau_spacing_x = 125 # The spacing between all Tableau Piles
        tableau_base_y = 300 # The Y position of all Tableau Piles
        vertical_offset = 25 # How far down each stacked card peaks out

        for column_index, column in enumerate(self.game.tableau):
            x = tableau_start_x + (column_index * tableau_spacing_x)
            for card_index, card in enumerate(column):
                y = tableau_base_y + (card_index * vertical_offset)

                photo_image = self.load_and_resize(card.image_filename())

                # Keep reference alive
                self.card_images.append(photo_image)

                self.canvas.create_image(x, y, image=photo_image, tags="card")
                
                # Store card position for card selection
                self.card_positions.append((card, x, y, column_index, card_index, "Tableau"))

        # Draws foundation cards if foundation contains cards
        foundation_start_x = 250
        foundation_spacing_x = 125
        foundation_y = 100

        for pile_index, pile in enumerate(self.game.foundations):
            if pile:
                top_card = pile[-1]
                x = foundation_start_x + (pile_index * foundation_spacing_x)

                photo_image = self.load_and_resize(top_card.image_filename())
                self.card_images.append(photo_image)
                self.canvas.create_image(x, foundation_y, image=photo_image, tags="card")
                
                # Store card position for card selection
                self.card_positions.append((top_card, x, foundation_y, pile_index, pile, "Foundation"))
                
        # Draws stock cards into stock
        if not self.game.stock:
            photo_image = self.ace_image
            self.card_images.append(photo_image)
            self.canvas.create_image(self.stock_x, self.stock_y, image=photo_image, tags="card")
            
            # Append Card to Card Positions
            self.card_positions.append((None, self.stock_x, self.stock_y, None, None, "Stock"))
            
        else:
            top_card = self.game.stock[-1]
            photo_image = self.load_and_resize(top_card.image_filename())
            self.card_images.append(photo_image)
            self.canvas.create_image(self.stock_x, self.stock_y, image=photo_image, tags="card")
            
            # Append Card to Card Positions
            self.card_positions.append((top_card, self.stock_x, self.stock_y, None, None, "Stock"))
            
        # Draws waste cards into stock
        if self.game.waste:
            top_card = self.game.waste[-1]
            photo_image = self.load_and_resize(top_card.image_filename())
            self.card_images.append(photo_image)
            self.canvas.create_image(self.waste_x, self.waste_y, image=photo_image, tags="card")
        
            # Append Card to Card Positions
            self.card_positions.append((top_card, self.waste_x, self.waste_y, None, None, "Waste"))
            
        

    # Function to handle card clicks
    def canvas_card_click(self, event):
        
        # Checks through card positions reversed
        for card, x, y, pile_index, card_index, pile_type in reversed(self.card_positions):
            
            # if the pile of this card is a tableau pile
            if(pile_type == "Tableau"):
                column = self.game.tableau[pile_index]
                index = len(column) - 1
                
                if (card_index != index):
                    continue
                
                if (not card.face_up):
                    continue
                 
            left = x - 50
            right = x + 50
            top = y - 80
            bottom = y + 80
                        
                
            # Is the click within x and y boundaries
            if (event.x > left and event.x < right) and (event.y > top and event.y < bottom):
                
                 return card
        
        return None
    
    # Function to handle toggle of card clicks
    def on_canvas_click(self, event):
        
        if (event.x > self.stock_x - 50 and event.x < self.stock_x + 50) and (event.y > self.stock_y - 80 and event.y < self.stock_y + 80):
            
            # Calls stock to waste logic
            self.game.stock_to_waste()
            
            # Clear current selections
            self.selected_card = None
            
            if self.canvas_ID is not None:
                self.canvas.delete(self.canvas_ID)
                self.canvas_ID = None
            
            # Recalls refresh board
            self.refresh_board()
            
            return

        # clicked card contains current clicked card details
        clicked_card = self.canvas_card_click(event)

        if not clicked_card:
            return None

        # IF card is same as selected card -> Deselect
        if self.selected_card == clicked_card:
            self.selected_card = None
            self.canvas.delete(self.canvas_ID)
            self.canvas_ID = None

        # Else Select Card
        else:
            self.selected_card = clicked_card
            
            if self.canvas_ID is not None:
                self.canvas.delete(self.canvas_ID)

            # Find X and Y coordinates of clicked card
            for card, x, y, pile_index, card_index, pile_type in self.card_positions:
                if card == clicked_card:
                    self.canvas_ID = self.canvas.create_rectangle(
                            x - 50,
                            y - 80,
                            x + 50,
                            y + 80,
                            outline="blue",
                            width=3
                    )
                    break       
        
    # Function to load and resize images (helper)
    def load_and_resize(self, filename):
        raw = Image.open(filename)
        resized = raw.resize((100, 160),
                Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized)

