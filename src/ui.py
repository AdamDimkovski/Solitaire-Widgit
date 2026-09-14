import tkinter as tk

from PIL import Image, ImageTk

class AppWindow:
    def __init__(self, root, game, click_callback):
        self.root = root
        self.root.title("Solitaire")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.game = game 
        
        # Save the callback function passed from main.py
        self.click_callback = click_callback

        # Tag which holds my background image
        self.bg_image = tk.PhotoImage(
            file="assets//Background//backgroundImage.png"
        )

        # Adds placeholder image for foundation cards and resizes them
        self.raw_card_placeholder = Image.open("assets//PNG//Cards//cardPlaceholder.png") 
        # Resizes Cards
        resized_img = self.raw_card_placeholder.resize((100, 160), Image.Resampling.LANCZOS)
        self.ace_image = ImageTk.PhotoImage(resized_img)

        # Adds drawpile image for drawpile and resizes it
        self.raw_card_placeholder = Image.open("assets//PNG//Cards//cardBack_red4.png")
        # Resizes Cards
        resized_img = self.raw_card_placeholder.resize((100, 160), Image.Resampling.LANCZOS)
        self.drawpile_image = ImageTk.PhotoImage(resized_img)

        # Create and place widgets
        self.create_widgets()
        
        
        
    # Function that creates UI widgits
    def create_widgets(self):

        # Create the game canvas
        self.canvas = tk.Canvas(
            self.root,
            width=1000,
            height=700,
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

        # Drawpile Card
        self.canvas.create_image(
            900,
            100,
            image=self.drawpile_image
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

    # Function to refresh cards on screen
    def refresh_board(self):

        # Clear previous render
        self.canvas.delete("card")
        self.card_images = []

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


    def load_and_resize(self, filename):
        raw = Image.open(filename)
        resized = raw.resize((100, 160),
                Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized)

