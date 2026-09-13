import tkinter as tk

class AppWindow:
    def __init__(self, root, click_callback):
        self.root = root
        self.root.title("Solitaire")
        self.root.geometry("1000x700")
        self.root.resizable(False, False) 
        
        # Save the callback function passed from main.py
        self.click_callback = click_callback
        
        self.bg_image = tk.PhotoImage(
            file="assets//Background//backgroundImage.png"
        )
        
        self.ace_image = tk.PhotoImage(
            file="assets//PNG//Cards//AcePlaceholder.png"
            )
        
        
        # Create and place widgets
        self.create_widgets()
        
        
        
        
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
        self.canvas.create_image(
            700,
            100,
            image=self.ace_image
        )

        self.canvas.create_image(
            770,
            100,
            image=self.ace_image
        )

        self.canvas.create_image(
            840,
            100,
            image=self.ace_image
        )

        self.canvas.create_image(
            910,
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
            width=15,
            height=3
        )

        self.button.place(x=15, y=15)
        
        