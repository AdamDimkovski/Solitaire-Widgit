import tkinter as tk
import random

from PIL import Image, ImageTk

class AppWindow:
    def __init__(self, root, game, click_callback):
        self.root = root
        self.root.title("Solitaire")
        
        
        # Everything is designed on a 1000x1000 grid, then scaled to the screen
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        self.win_size = int(min(screen_w, screen_h) * 0.85)  # 0.85 leaves room for taskbar/title bar
        self.scale = self.win_size / 1000

        self.card_w = self.sc(100)
        self.card_h = self.sc(160)
        self.half_w = self.card_w // 2
        self.half_h = self.card_h // 2
        self.col_spacing = self.sc(125)
        self.stack_offset = self.sc(25)
        self.top_row_y = self.sc(100)
        self.tableau_x = self.sc(125)
        self.tableau_y = self.sc(300)
        self.foundation_x = self.sc(250)
        self.stock_x = self.sc(900)
        self.stock_y = self.top_row_y
        self.waste_x = self.sc(750)
        self.waste_y = self.top_row_y
        
        self.root.geometry(f"{self.win_size}x{self.win_size}")
        self.root.resizable(False, False)
        self.game = game 
        
        # Card Highlighting Variables
        self.selected_card = None
        self.source_pile = None
        self.pile_number = None
        self.card_index_inpile = None
        self.canvas_ID = None
        self.card_positions = []
        self.card_images = []
        
        self.game_won = False
        self.anim_after_id = None
        self.launch_queue = []
        self.flying_cards = []
        self.win_images = []
        self.win_text_id = None
        self.tick = 0
        self.trail_layer = None
        self.trail_photo = None
        self.trail_id = None
        
        # Save the callback function passed from main.py
        self.click_callback = click_callback

        # Tag which holds my background image
        bg_raw = Image.open("assets//Background//backgroundImage.jpg")
        self.bg_image = ImageTk.PhotoImage(
            bg_raw.resize((self.win_size, self.win_size), Image.Resampling.LANCZOS)
        )

        # Adds placeholder image for foundation cards and resizes them
        self.ace_image = self.load_and_resize("assets//PNG//Cards//cardPlaceholder.png")

        # Adds drawpile image for drawpile and resizes it
        self.drawpile_image = self.load_and_resize("assets//PNG//Cards//cardBack_red4.png")

        # Create and place widgets
        self.create_widgets()
        
        self.refresh_board()
        
        self.root.bind("w", self.cheat_win)
        
        
    # Function that creates UI widgits
    def create_widgets(self):

        # Create the game canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.win_size,
            height=self.win_size,
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

        # New Game button
        self.button = tk.Button(
            self.root,
            text="New Game",
            command=self.click_callback,
            font=("Arial", max(10, self.sc(16)), "bold"),
            bg="#222222",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            relief="flat",
            bd=0,
            width=12,
            height=2
        )

        self.button.place(x=self.sc(15), y=self.sc(15))

        # Foundation Piles
        for i in range(4):
            self.canvas.create_image(self.foundation_x + i * self.col_spacing, self.top_row_y, image=self.ace_image)

        # Tableau Piles
        for i in range(7):
            self.canvas.create_image(self.tableau_x + i * self.col_spacing, self.tableau_y, image=self.ace_image)
        
            
        # Card Click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    # Function to refresh cards on screen
    def refresh_board(self):
        
        # Stop and clear any win animation
        if self.anim_after_id is not None:
            self.root.after_cancel(self.anim_after_id)
            self.anim_after_id = None

        self.canvas.delete("win")
        self.canvas.delete("wintext")
        self.launch_queue = []
        self.flying_cards = []
        self.win_images = []
        self.win_text_id = None
        self.game_won = False
        self.tick = 0
        self.trail_layer = None
        self.trail_photo = None
        self.trail_id = None

        # Clear previous render
        self.canvas.delete("card")
        self.card_images = []
        
        self.card_positions = []
        
        # Handles reseting selected cards if game restarts
        self.selected_card = None
        self.source_pile = None
        self.pile_number = None
        self.card_index_inpile = None

        if self.canvas_ID is not None:
            self.canvas.delete(self.canvas_ID)

        self.canvas_ID = None

        for column_index, column in enumerate(self.game.tableau):
            x = self.tableau_x + (column_index * self.col_spacing)
            for card_index, card in enumerate(column):
                y = self.tableau_y + (card_index * self.stack_offset)

                photo_image = self.load_and_resize(card.image_filename())

                # Keep reference alive
                self.card_images.append(photo_image)

                self.canvas.create_image(x, y, image=photo_image, tags="card")
                
                # Store card position for card selection
                self.card_positions.append((card, x, y, column_index, card_index, "Tableau"))

        for pile_index, pile in enumerate(self.game.foundations):
            if pile:
                top_card = pile[-1]
                x = self.foundation_x + (pile_index * self.col_spacing)

                photo_image = self.load_and_resize(top_card.image_filename())
                self.card_images.append(photo_image)
                self.canvas.create_image(x, self.top_row_y, image=photo_image, tags="card")
                
                # Store card position for card selection
                self.card_positions.append((top_card, x, self.top_row_y, pile_index, len(pile) - 1, "Foundation"))
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
                
                if (not card.face_up):
                    continue
                 
            left = x - self.half_w
            right = x + self.half_w
            top = y - self.half_h
            bottom = y + self.half_h
            
            # Stock loop block
            if(pile_type == "Stock"):
                continue
                        
            # Is the click within x and y boundaries
            if (event.x > left and event.x < right) and (event.y > top and event.y < bottom):
                
                 return card, pile_type, pile_index, card_index
        
        return None
    
    # Function to handle toggle of card clicks
    def on_canvas_click(self, event):
        
        if self.game_won:
            return
        
        if (event.x > self.stock_x - self.half_w and event.x < self.stock_x + self.half_w) and (event.y > self.stock_y - self.half_h and event.y < self.stock_y + self.half_h):
            
            # Calls stock to waste logic
            self.game.stock_to_waste()
            
            # Clear current selections
            self.selected_card = None
            self.source_pile = None
            self.pile_number = None
            self.card_index_inpile = None
            
            if self.canvas_ID is not None:
                self.canvas.delete(self.canvas_ID)
                self.canvas_ID = None
            
            # Recalls refresh board
            self.refresh_board()
            
            return

        # clicked card contains current clicked card details
        clicked_info = self.canvas_card_click(event)
        
        if self.selected_card is not None:
            identifier = self.pile_identifier(event)
            
            if identifier is not None:
               destination_type, destination_number = identifier
                
               if self.game.card_moving(self.source_pile, self.pile_number, self.card_index_inpile, destination_type, destination_number):
                   self.refresh_board()
                   
                   # Checks to see if game win condition met for victory screen
                   if self.game.check_win():
                       self.show_win_screen()
                   return 

        if not clicked_info:
            self.selected_card = None
            self.source_pile = None
            self.pile_number = None
            self.card_index_inpile = None
            self.canvas.delete(self.canvas_ID)
            self.canvas_ID = None
            return None
        
        clicked_card, clicked_type, clicked_pile, clicked_index = clicked_info
        
        # IF card is same as selected card -> Deselect
        if self.selected_card == clicked_card or clicked_card == None:
            self.selected_card = None
            self.source_pile = None
            self.pile_number = None
            self.card_index_inpile = None
            self.canvas.delete(self.canvas_ID)
            self.canvas_ID = None       

        # Else Select Card
        else:
            self.selected_card = clicked_card
            self.source_pile = clicked_type
            self.pile_number = clicked_pile
            self.card_index_inpile = clicked_index
            
            if self.canvas_ID is not None:
                self.canvas.delete(self.canvas_ID)

            # Find X and Y coordinates of clicked card
            for card, x, y, pile_index, card_index, pile_type in self.card_positions:
                if card == clicked_card:
                    if pile_type == "Tableau":
                        cards_below = len(self.game.tableau[pile_index]) - 1 - card_index
                    else:
                        cards_below = 0

                    self.canvas_ID = self.canvas.create_rectangle(
                        x - self.half_w,
                        y - self.half_h,
                        x + self.half_w,
                        y + self.half_h + (self.stack_offset * cards_below),
                        outline="blue",
                        width=3
                    )
                    break    
        
    # Function to load and resize images (helper)
    def load_and_resize(self, filename):
        raw = Image.open(filename)
        resized = raw.resize((self.card_w, self.card_h),
                Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized)
    
    # Function to determine which pile was clicked (helper)
    def pile_identifier(self, event):

        for pile_numbers in range(4):
            x = self.foundation_x + (pile_numbers * self.col_spacing)
            y = self.top_row_y

            if (event.x > x - self.half_w and event.x < x + self.half_w) and (event.y > y - self.half_h and event.y < y + self.half_h):
                return "Foundation", pile_numbers

        for column_index, column in enumerate(self.game.tableau):
            x = self.tableau_x + (column_index * self.col_spacing)

            top_edge = self.tableau_y - self.half_h
            cards_after_first = max(len(column) - 1, 0)
            bottom_edge = self.tableau_y + (self.stack_offset * cards_after_first) + self.half_h

            if (event.x > x - self.half_w and event.x < x + self.half_w) and (event.y > top_edge and event.y < bottom_edge):
                return "Tableau", column_index

        return None
    
    # Detects victory condition + loads victory animation
    def show_win_screen(self):
        
        self.game_won = True
        self.launch_queue = []
        
        
        for pos in range(12, -1, -1):
            for index, pile in enumerate(self.game.foundations):
                
                self.launch_queue.append((pile[pos], index))
            
        # Banner behind the text so it stays readable over the trails
        s = self.sc

        self.canvas.create_rectangle(
            s(180), s(440), s(820), s(560),
            fill="#1b2a41", outline="#f4c542", width=max(2, s(4)),
            tags="wintext"
        )

        self.canvas.create_text(
            s(503), s(478), text="YOU WIN!",
            font=("Georgia", max(14, s(44)), "bold"),
            fill="black", anchor="center", tags="wintext"
        )

        self.win_text_id = self.canvas.create_text(
            s(500), s(475), text="YOU WIN!",
            font=("Georgia", max(14, s(44)), "bold"),
            fill="#f4c542", anchor="center", tags="wintext"
        )

        self.canvas.create_text(
            s(500), s(530), text="Press New Game to play again",
            font=("Arial", max(9, s(18))),
            fill="white", anchor="center", tags="wintext"
        )

        self.trail_layer = Image.new("RGBA", (self.win_size, self.win_size), (0, 0, 0, 0))
        self.trail_photo = ImageTk.PhotoImage(self.trail_layer)
        self.trail_id = self.canvas.create_image(
            0, 0, image=self.trail_photo, anchor="nw", tags="win"
        )

        self.animate_cards()
        
    # Plays victory animation
    def animate_cards(self):

        self.tick += 1
        stamped = False

        # Launch the next card every 15 ticks (first one launches immediately)
        if self.launch_queue and self.tick % 15 == 1:
            card, pile_index = self.launch_queue.pop(0)

            x = self.foundation_x + pile_index * self.col_spacing
            y = self.top_row_y

            pil_img = self.load_pil(card.image_filename())
            photo = ImageTk.PhotoImage(pil_img)
            self.win_images.append(photo)
            image_id = self.canvas.create_image(x, y, image=photo, tags="win")

            vx = random.randint(2, 6) * random.choice([-1, 1]) * self.scale
            vy = -3 * self.scale

            # Index 5 = photo (keeps reference alive), index 6 = Pillow image (for trails)
            self.flying_cards.append([image_id, x, y, vx, vy, photo, pil_img])

        for flying_card in self.flying_cards[:]:

            # Paint a trail copy onto the single trail layer every 3rd tick
            if self.tick % 3 == 0:
                self.trail_layer.paste(
                    flying_card[6],
                    (int(flying_card[1] - self.half_w), int(flying_card[2] - self.half_h)),
                    flying_card[6]
                )
                stamped = True

            # Keep the live card above the trail layer
            self.canvas.tag_raise(flying_card[0])

            # Gravity and movement
            flying_card[4] += 0.5 * self.scale
            flying_card[1] += flying_card[3]
            flying_card[2] += flying_card[4]

            # Bounce off the floor
            if flying_card[2] + self.half_h > self.win_size:
                flying_card[2] = self.win_size - self.half_h
                flying_card[4] = -flying_card[4] * 0.8

            # Retire once fully off the left or right side
            if flying_card[1] < -self.half_w or flying_card[1] > self.win_size + self.half_w:
                self.canvas.delete(flying_card[0])
                self.flying_cards.remove(flying_card)
                continue

            self.canvas.coords(flying_card[0], flying_card[1], flying_card[2])

        # Push the updated trails to the screen once per tick, not once per card
        if stamped:
            self.trail_photo.paste(self.trail_layer)

        # Keep the win text above everything
        self.canvas.tag_raise("wintext")

        if self.launch_queue or self.flying_cards:
            self.anim_after_id = self.root.after(16, self.animate_cards)
        else:
            self.anim_after_id = None
            
    # Returns a resized Pillow image (used for pasting trails)
    def load_pil(self, filename):
        img = Image.open(filename).convert("RGBA")
        return img.resize((self.card_w, self.card_h), Image.Resampling.LANCZOS)
        
            # TEMP CHEAT: delete when done testing
    def cheat_win(self, event):
        if self.game_won:
            return

        self.game.cheat_fill_foundations()
        self.refresh_board()

        if self.game.check_win():
            self.show_win_screen()
            
    # Scales a number from the 1000x1000 design grid to this screen
    def sc(self, n):
        return int(n * self.scale)