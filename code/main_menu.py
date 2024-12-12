import tkinter as tk


class MainMenu:
    def __init__(self, root, menu_callback):
        self.root = root
        self.menu_callback = menu_callback
        self.root.title("A Symphony of Stocks")
        self.root.geometry("680x480")
        self.root.config(bg="#f0f8ff")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="A Symphony of Stocks", font=("Garamond", 40), bg="#f0f8ff")
        label.pack(pady=50)

        play_button = tk.Button(self.root, text="Play", font=("Lato", 14),
                                command=lambda: self.menu_callback("play"))
        play_button.pack(pady=10)

        start_button = tk.Button(self.root, text="Start Tutorial", font=("Lato", 14),
                                 command=lambda: self.menu_callback("tutorial"))
        start_button.pack(pady=10)

        settings_button = tk.Button(self.root, text="Settings", font=("Lato", 14),
                                    command=lambda: self.menu_callback("settings"))
        settings_button.pack(pady=10)

        footer_label = tk.Label(self.root, text="© 2024 A Symphony of Stocks", font=("Arial", 10), fg="#888",
                                bg="#f0f8ff")
        footer_label.pack(side="bottom", pady=10)
