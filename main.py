from audio.sound_manager import SoundManager
from data.stock_data import StockData
from game_logic.market import Market
from ui.GUI import StockMarketUI

def main():
    stock_data = StockData.load_data("data/UK_FTSE100 Index.csv")
    market = Market(initial_money=100000.0)  # Initial balance set to $100,000

    sound_manager = SoundManager("audio", stock_data['Close'][0])
    ui = StockMarketUI(market, stock_data, sound_manager)
    ui.show_instruction_window()

if __name__ == "__main__":
    main()
