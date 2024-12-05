from audio.sound_manager import SoundManager
from data.stock_data import StockData
from game_logic.market import Market
from ui.GUI import StockMarketUI

def main():
    # 加载股票数据
    stock_data = StockData.load_data("data/stock_data.csv")
    
    # 初始化市场和音频管理器
    market = Market(initial_money=1000.0)
    sound_manager = SoundManager("audio")

    # 启动用户界面
    ui = StockMarketUI(market, stock_data, sound_manager)
    ui.create_main_window()



if __name__ == "__main__":
    main()
    ui.start_ui()
