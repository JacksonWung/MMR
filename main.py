from code.sound_manager import SoundManager
from code.stock_data import StockData
from code.market import Market
from code.GUI import StockMarketUI

def main():
    stock_data = StockData.load_data("data/UK_FTSE100 Index.csv")
    market = Market(initial_money=100000.0)  # Initial balance set to $100,000

    sound_manager = SoundManager("audio", stock_data['Close'][0])
    ui = StockMarketUI(market, stock_data, sound_manager)
    ui.show_instruction_window()

if __name__ == "__main__":
    main()
