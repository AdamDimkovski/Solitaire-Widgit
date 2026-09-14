import tkinter as tk
from game import Game
from ui import AppWindow  # ui.py

def start_new_game(game, app_window):
    game.new_game()
    app_window.refresh_board()

def handle_button_action():
    print("The button was clicked! Logic processed in main.py.")
    
def main():
    root = tk.Tk()
    game = Game()
    app = AppWindow(root, game, click_callback=lambda: start_new_game(game, app))
    root.mainloop()
    
if __name__ == "__main__":
    main()
