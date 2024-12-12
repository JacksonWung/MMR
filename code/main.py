import tkinter as tk
from sound_manager import SoundManager
from stock_data import StockData
from market import Market
from GUI import StockMarketUI
from main_menu import MainMenu
from tutorial import TutorialWindow
from settings_menu import SettingsMenu

# Global variables to store the selected stock file and initial money
stock_file = "AAPL.csv"  # Default stock file
initial_money = 100000.0  # Default initial money

# Modify the settings callback to update global values
def settings_callback(selected_stock_file, updated_money):
    global stock_file, initial_money  # Access global variables

    # Update the global values
    stock_file = selected_stock_file
    initial_money = updated_money

    print(f"Selected Stock Data: {stock_file}")
    print(f"Initial Money: ${initial_money}")


def menu_selection(option, root, stock_data, sound_manager):
    global stock_file, initial_money  # Access global variables

    if option == "play":
        root.destroy()  # Close the main menu

        # Reload stock data using the updated stock_file
        stock_data = StockData.load_data(stock_file)

        # Create a new market instance with the updated initial money
        market = Market(initial_money=initial_money)

        # Launch the game UI
        ui = StockMarketUI(market, stock_data, sound_manager)
        ui.create_main_window()

    elif option == "tutorial":
        root.destroy()

        def start_game():
            # Reload stock data using the updated stock_file
            stock_data = StockData.load_data(stock_file)

            # Launch the game UI
            ui = StockMarketUI(market, stock_data, sound_manager)
            ui.create_main_window()

        tutorial = TutorialWindow(start_game)
        tutorial.show_instruction_window()

    elif option == "settings":
        settings_window = tk.Toplevel(root)
        settings_menu = SettingsMenu(settings_window, settings_callback)  # Pass the updated callback
    else:
        print("Invalid choice.")


def main():
    global stock_file  # Use the global stock_file variable
    global initial_money  # Use the global initial_money variable

    # Initially load stock data (this will be updated after settings are applied)
    stock_data = StockData.load_data(stock_file)
    sound_manager = SoundManager("audio", stock_data['Close'][0])

    # Create main menu
    root = tk.Tk()
    root.title("Main Menu")
    menu = MainMenu(root, lambda option: menu_selection(option, root, stock_data, sound_manager))
    root.mainloop()


if __name__ == "__main__":
    main()