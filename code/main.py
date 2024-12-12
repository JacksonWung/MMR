import tkinter as tk
from sound_manager import SoundManager
from stock_data import StockData
from market import Market
from GUI import StockMarketUI
from main_menu import MainMenu
from tutorial import TutorialWindow


def menu_selection(option, root, stock_data, sound_manager):
    market = Market(initial_money=100000.0)
    if option == "play":
        root.destroy()  # Close the main menu
        ui = StockMarketUI(market, stock_data, sound_manager)
        ui.create_main_window()
    elif option == "tutorial":
        root.destroy()
        def start_game():
            ui = StockMarketUI(market, stock_data, sound_manager)
            ui.create_main_window()
        tutorial = TutorialWindow(start_game)
        tutorial.show_instruction_window()
    elif option == "settings":
        # Launch settings logic
        print("Settings selected. Show settings window here.")
    else:
        print("Invalid choice.")


def main():
    stock_data = StockData.load_data("UK_FTSE100 Index.csv")
    sound_manager = SoundManager("audio", stock_data['Close'][0])

    # Create main menu
    root = tk.Tk()
    root.title("Main Menu")
    menu = MainMenu(root, lambda option: menu_selection(option, root, stock_data, sound_manager))
    root.mainloop()


if __name__ == "__main__":
    main()
