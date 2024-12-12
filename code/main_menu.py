import tkinter as tk


class MainMenu:
    def __init__(self, root, stock_ui):
        self.root = root
        self.stock_ui = stock_ui
        self.root.title("A Symphony of Stocks")

        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="A Symphony of Stocks", font=("Helvetica", 16))
        label.pack(pady=10)

        play_button = tk.Button(self.root, text="Play", command=self.stock_ui.play_game)
        play_button.pack(pady=5)

        start_button = tk.Button(self.root, text="Start", command=self.stock_ui.start_game)
        start_button.pack(pady=5)

        settings_button = tk.Button(self.root, text="Settings", command=self.stock_ui.open_settings)
        settings_button.pack(pady=5)
