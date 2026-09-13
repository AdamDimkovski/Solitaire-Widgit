import tkinter as tk
from ui import AppWindow  # ui.py


def handle_button_action():
    print("The button was clicked! Logic processed in main.py.")
    
def main():
    root = tk.Tk()
    
    app = AppWindow(root, click_callback=handle_button_action)
    
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
