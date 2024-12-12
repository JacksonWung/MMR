import os
import tkinter as tk
from tkinter import messagebox

class SettingsMenu:
    def __init__(self, root, settings_callback):
        self.root = root
        self.settings_callback = settings_callback
        self.root.title("Settings - A Symphony of Stocks")

        # Set a larger window size
        self.root.geometry("600x400")

        # Set a background color
        self.root.config(bg="#f2f2f2")

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        label = tk.Label(self.root, text="Settings", font=("Arial", 24, "bold"), fg="#4CAF50", bg="#f2f2f2")
        label.pack(pady=20)

        # Stock Data selection (Drop-down)
        self.stock_data_label = tk.Label(self.root, text="Select Stock Data:", font=("Arial", 12), fg="#333", bg="#f2f2f2")
        self.stock_data_label.pack(pady=10)

        # List all CSV files in the 'data' directory (correct relative path)
        self.stock_data_options = self.get_csv_files_in_directory("../data")  # Go up one level and then into the 'data' folder
        if not self.stock_data_options:
            messagebox.showerror("Error", "No CSV files found in the 'data' folder.")
            return

        self.stock_data_var = tk.StringVar()
        self.stock_data_var.set(self.stock_data_options[0])  # Default selection

        self.stock_data_menu = tk.OptionMenu(self.root, self.stock_data_var, *self.stock_data_options)
        self.stock_data_menu.config(font=("Arial", 12), width=20)
        self.stock_data_menu.pack(pady=10)

        # Initial Money input
        self.initial_money_label = tk.Label(self.root, text="Initial Money ($):", font=("Arial", 12), fg="#333", bg="#f2f2f2")
        self.initial_money_label.pack(pady=10)

        self.initial_money_var = tk.DoubleVar()
        self.initial_money_var.set(100000)  # Default amount of initial money

        self.initial_money_entry = tk.Entry(self.root, textvariable=self.initial_money_var, font=("Arial", 12), width=20)
        self.initial_money_entry.pack(pady=10)

        # Apply button to save settings
        self.apply_button = tk.Button(self.root, text="Apply Settings", command=self.apply_settings,
                                      font=("Arial", 14), fg="#fff", bg="#4CAF50", relief="solid", padx=20, pady=10, bd=0)
        self.apply_button.pack(pady=20)

        # Go Back button
        self.back_button = tk.Button(self.root, text="Back", command=self.go_back,
                                      font=("Arial", 14), fg="#fff", bg="#FF5722", relief="solid", padx=20, pady=10, bd=0)
        self.back_button.pack(pady=10)

    def get_csv_files_in_directory(self, directory):
        """Return a list of CSV filenames in the specified directory."""
        try:
            # Get all files in the directory
            files = os.listdir(directory)
            # Filter only CSV files
            csv_files = [file for file in files if file.endswith(".csv")]
            return csv_files
        except FileNotFoundError:
            messagebox.showerror("Error", f"The directory '{directory}' does not exist.")
            return []

    def apply_settings(self):
        stock_data = self.stock_data_var.get()
        initial_money = self.initial_money_var.get()

        # Validate initial money input
        if initial_money <= 0:
            messagebox.showerror("Invalid Input", "Initial money must be a positive number.")
            return

        # Call the settings callback to pass the settings back
        self.settings_callback(stock_data, initial_money)

    def go_back(self):
        # Go back to the main menu (this is just an example, modify according to your app)
        self.root.destroy()  # Close the settings menu to go back to the main menu

# Example callback function to test the settings menu
def settings_callback(stock_data, initial_money):
    print(f"Selected Stock Data: {stock_data}")
    print(f"Initial Money: ${initial_money}")

if __name__ == "__main__":
    root = tk.Tk()
    settings_menu = SettingsMenu(root, settings_callback)
    root.mainloop()