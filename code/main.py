from sound_manager import SoundManager
from stock_data import StockData
from market import Market
from GUI import StockMarketUI


def main():
    stock_data = StockData.load_data("UK_FTSE100 Index.csv")
    market = Market(initial_money=100000.0)  # Initial balance set to $100,000

    sound_manager = SoundManager("audio", stock_data['Close'][0])
    ui = StockMarketUI(market, stock_data, sound_manager)
    ui.show_instruction_window()


if __name__ == "__main__":
    main()
