import pandas as pd
import numpy as np
import pygame
import tkinter as tk
from tkinter import messagebox
import threading
import time


pygame.init()
pygame.mixer.init()


NOTE_A4_SOUND = pygame.mixer.Sound("audio/A4.wav")
NOTE_B4_SOUND = pygame.mixer.Sound("audio/B4.wav")
NOTE_C5_SOUND = pygame.mixer.Sound("audio/C5.wav")
NOTE_A4 = "A4"  
NOTE_B4 = "B4"  
NOTE_C5 = "C5"  
# 玩家初始资金和库存
player_money = 1000.0  # 初始资金
player_stocks = 0  # 初始股票数量
stop_thread = False  # 用于停止音乐线程
music_thread = None  # 当前音乐线程对象
paused = False  # 全局变量，控制暂停状态


def play_sound(note):
    duration = 500  
    if note == NOTE_A4:
        NOTE_A4_SOUND.play()
    elif note == NOTE_B4:
        NOTE_B4_SOUND.play()
    elif note == NOTE_C5:
        NOTE_C5_SOUND.play()

def price_to_frequency(price, prev_price):
    """
    根据价格波动映射音调。
    """
    if price > prev_price:
        return NOTE_C5  # 价格上升映射为高音
    elif price < prev_price:
        return NOTE_A4  # 价格下降映射为低音
    else:
        return NOTE_B4  # 价格不变映射为中音

def play_stock_music(prices, interval, dates, min_price, max_price, repeat=3):
    """
    播放股票价格对应的音乐。
    """
    global today, stop_thread, paused
    for _ in range(repeat):
        for i in range(1, len(prices)):
            if stop_thread:  # 停止线程
                return
            while paused:  # 如果暂停，则等待
                time.sleep(0.1)
            price = prices[i]
            prev_price = prices[i - 1]
            # 根据价格增量映射音符
            note = price_to_frequency(price, prev_price)
            play_sound(note)  # 播放音符
            today = dates[i].strftime("%m/%d/%Y")  # 更新日期
            time.sleep(interval)  # 音符间隔

# Function to calculate harmonizing and dissonant notes
def calculate_note_frequencies(base_note):
    # For this code, you can define harmonizing/dissonant frequencies if needed
    pass  # Placeholder for potential harmonizing notes

# Function to evaluate buy opportunities
def evaluate_buy_opportunities(df):
    buy_opportunities = []
    for i in range(1, len(df)):
        if df['Close'][i] > df['Close'][i - 1]:
            buy_opportunities.append((df['Date'][i], True))  # Good buy
        else:
            buy_opportunities.append((df['Date'][i], False))  # Bad buy
    return buy_opportunities

# Function to handle button click
def on_buy_button_click(date):
    if date in buy_dates:
        is_good_buy = buy_dates[date]
        base_note = NOTE_A4  # Base note for the piano sound
        if is_good_buy:
            play_sound(base_note)  # Play the base note for a good buy
            messagebox.showinfo("Buy Opportunity", f"Good buy opportunity on {date}!")
        else:
            play_sound(NOTE_B4)  # Play a different note for a bad buy
            messagebox.showwarning("Buy Opportunity", f"Bad buy opportunity on {date}.")
    else:
        messagebox.showwarning("No Opportunity", "No buy opportunity for today.")

def on_buy_button_click(date, price):
    global player_money, player_stocks
    if player_money >= price:
        player_money -= price
        player_stocks += 1
        messagebox.showinfo("Buy", f"Bought 1 stock at {price}. Remaining money: {player_money:.2f}")
    else:
        messagebox.showwarning("Buy Failed", "Not enough money to buy this stock.")

def on_sell_button_click(price):
    global player_money, player_stocks
    if player_stocks > 0:
        player_money += price
        player_stocks -= 1
        messagebox.showinfo("Sell", f"Sold 1 stock at {price}. Total money: {player_money:.2f}")
    else:
        messagebox.showwarning("Sell Failed", "No stocks to sell.")

def create_gui(buy_opportunities, df):
    global buy_dates, music_thread, stop_thread, player_money, player_stocks, paused
    buy_dates = {date.strftime("%m/%d/%Y"): is_good_buy for date, is_good_buy in buy_opportunities}

    # 创建主窗口
    window = tk.Tk()
    window.title("Stock Market Musical Score")
    window.geometry("400x400")  # 调整窗口大小
    window.configure(bg="#f0f0f0")  # 设置背景颜色

    # 居中窗口
    window.eval('tk::PlaceWindow . center')

    # 显示玩家资金和库存的区域
    info_frame = tk.Frame(window, bg="#f0f0f0")
    info_frame.pack(pady=10)

    money_label = tk.Label(info_frame, text=f"Money: ${player_money:.2f}", font=("Arial", 12), bg="#f0f0f0")
    money_label.grid(row=0, column=0, padx=10, pady=5)

    stock_label = tk.Label(info_frame, text=f"Stocks: {player_stocks}", font=("Arial", 12), bg="#f0f0f0")
    stock_label.grid(row=0, column=1, padx=10, pady=5)

    # 定期刷新资金和库存信息
    def update_labels():
        money_label.config(text=f"Money: ${player_money:.2f}")
        stock_label.config(text=f"Stocks: {player_stocks}")
        window.after(1000, update_labels)  # 每秒刷新一次

    update_labels()

    # 停止游戏逻辑
    def stop_game():
        global stop_thread, paused, music_thread
        stop_thread = True  # 设置停止标志
        paused = False  # 停止后自动取消暂停
        if music_thread and music_thread.is_alive():
            music_thread.join(timeout=1)  # 等待线程结束
        music_thread = None  # 清理线程对象
        messagebox.showinfo("Game Stopped", "The game has been stopped!")

    # 恢复音乐播放逻辑
    def resume_game():
        global paused, stop_thread, music_thread
        if stop_thread:
            messagebox.showerror("Error", "Game is stopped. Use Restart to start again.")
            return
        paused = False  # 取消暂停
        if not music_thread or not music_thread.is_alive():
            music_thread = threading.Thread(target=play_stock_music, args=(prices, interval, dates, min_price, max_price, repeat))
            music_thread.start()
        messagebox.showinfo("Game Resumed", "The game has been resumed!")

    # 暂停游戏逻辑
    def pause_game():
        global paused
        paused = True
        messagebox.showinfo("Game Paused", "The game has been paused!")

    # 重新开始游戏逻辑
    def restart_game():
        global stop_thread, music_thread, player_money, player_stocks
        stop_game()  # 停止旧线程
        stop_thread = False  # 重置停止标志
        player_money = 1000.0  # 重置玩家资金
        player_stocks = 0  # 重置玩家库存
        music_thread = threading.Thread(target=play_stock_music, args=(prices, interval, dates, min_price, max_price, repeat))
        music_thread.start()  # 启动新线程
        messagebox.showinfo("Game Restarted", "The game has been restarted!")

    # 窗口关闭事件绑定
    def on_close():
        stop_game()  # 停止音乐线程
        window.destroy()  # 销毁窗口

    window.protocol("WM_DELETE_WINDOW", on_close)

    # 当前日期和价格的显示
    price_frame = tk.Frame(window, bg="#f0f0f0")
    price_frame.pack(pady=10)

    date_label = tk.Label(price_frame, text="Date: ", font=("Arial", 12), bg="#f0f0f0")
    date_label.grid(row=0, column=0, padx=10, pady=5)

    global today
    today = buy_opportunities[-1][0].strftime("%m/%d/%Y")
    date_label.config(text=f"Date: {today}")

    price_label = tk.Label(price_frame, text="Current Price: $0.00", font=("Arial", 12), bg="#f0f0f0")
    price_label.grid(row=0, column=1, padx=10, pady=5)

    # 获取当前价格
    def get_current_price():
        current_date = pd.to_datetime(today, format="%m/%d/%Y")
        current_row = df.loc[df['Date'] == current_date]
        if not current_row.empty:
            return current_row['Close'].iloc[0]
        return None

    def update_price():
        current_price = get_current_price()
        if current_price is not None:
            price_label.config(text=f"Current Price: ${current_price:.2f}")
        else:
            price_label.config(text="No price available")
        window.after(1000, update_price)  # 每秒刷新一次价格

    update_price()

    # 按钮区域
    button_frame = tk.Frame(window, bg="#f0f0f0")
    button_frame.pack(pady=20)

    buy_button = tk.Button(button_frame, text="Buy", font=("Arial", 12), bg="#d1ffd1", fg="black",
                        command=lambda: on_buy_button_click(today, get_current_price()))
    buy_button.grid(row=0, column=0, padx=10, pady=5)

    sell_button = tk.Button(button_frame, text="Sell", font=("Arial", 12), bg="#ffd1d1", fg="black",
                            command=lambda: on_sell_button_click(get_current_price()))
    sell_button.grid(row=0, column=1, padx=10, pady=5)

    # 控制按钮区域
    control_frame = tk.Frame(window, bg="#f0f0f0")
    control_frame.pack(pady=10)

    stop_button = tk.Button(control_frame, text="Stop", font=("Arial", 12), bg="#ffcccc", fg="black", command=stop_game)
    stop_button.grid(row=0, column=0, padx=10, pady=5)

    restart_button = tk.Button(control_frame, text="Restart", font=("Arial", 12), bg="#ccffcc", fg="black", command=restart_game)
    restart_button.grid(row=0, column=1, padx=10, pady=5)

    resume_button = tk.Button(control_frame, text="Resume", font=("Arial", 12), bg="#ccff99", fg="black", command=resume_game)
    resume_button.grid(row=0, column=2, padx=10, pady=5)

    pause_button = tk.Button(control_frame, text="Pause", font=("Arial", 12), bg="#ffffcc", fg="black", command=pause_game)
    pause_button.grid(row=0, column=3, padx=10, pady=5)

    window.mainloop()


market_orders = []  # 市场订单队列

def add_order(order_type, price, volume):
    market_orders.append({'type': order_type, 'price': price, 'volume': volume})
    market_orders.sort(key=lambda x: x['price'])  # 根据价格排序

def process_orders():
    global market_orders, player_money, player_stocks
    for order in market_orders:
        if order['type'] == 'sell' and player_money >= order['price']:
            # 玩家购买订单
            player_money -= order['price']
            player_stocks += order['volume']
            market_orders.remove(order)
            messagebox.showinfo("Market", f"Bought {order['volume']} stocks at {order['price']}.")
        elif order['type'] == 'buy' and player_stocks >= order['volume']:
            # 玩家出售订单
            player_money += order['price']
            player_stocks -= order['volume']
            market_orders.remove(order)
            messagebox.showinfo("Market", f"Sold {order['volume']} stocks at {order['price']}.")

def main():
    global music_thread, prices, interval, dates, min_price, max_price, repeat

    # 加载CSV数据
    df = pd.read_csv("data/stock_data.csv")
    df['Close'] = df['Close'].replace({'"': '', ',': ''}, regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    # 动态计算价格范围
    min_price = df['Close'].min()
    max_price = df['Close'].max()

    # 生成买入机会
    buy_opportunities = evaluate_buy_opportunities(df)

    # 音乐播放参数
    interval = 2.0
    repeat = 5
    prices = df['Close'].tolist()
    dates = df['Date'].tolist()

    # 启动音乐线程
    music_thread = threading.Thread(target=play_stock_music, args=(prices, interval, dates, min_price, max_price, repeat))
    music_thread.start()

    # 创建GUI界面
    create_gui(buy_opportunities, df)

if __name__ == "__main__":
    main()
