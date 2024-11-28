import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time
import threading


class StockMarketUI:
    def __init__(self, market, stock_data, sound_manager):
        self.market = market
        self.stock_data = stock_data
        self.sound_manager = sound_manager
        self.prices = stock_data['Close'].tolist()
        self.dates = stock_data['Date'].tolist()
        self.index = 0
        self.stop_thread = False

    def create_main_window(self):
        window = tk.Tk()
        window.title("Stock Market Simulator")
        window.geometry("800x600")

        # 曲线图
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_title("Stock Price Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        self.line, = ax.plot([], [], color="blue")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack()

        # 玩家资金和仓位信息
        self.money_label = tk.Label(window, text=f"Money: ${self.market.player_money:.2f}", font=("Arial", 12))
        self.money_label.pack()

        self.stock_label = tk.Label(window, text=f"Stocks: {self.market.player_stocks}", font=("Arial", 12))
        self.stock_label.pack()

        self.total_label = tk.Label(window, text=f"Total Value: ${self.calculate_total_value():.2f}", font=("Arial", 12))
        self.total_label.pack()

        # 当前价格显示
        self.price_label = tk.Label(window, text="Current Price: $0.00", font=("Arial", 12))
        self.price_label.pack()

        # 买卖功能
        control_frame = tk.Frame(window)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Quantity:").grid(row=0, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(control_frame, width=10)
        self.quantity_entry.grid(row=0, column=1, padx=5, pady=5)

        buy_button = tk.Button(control_frame, text="Buy", command=self.buy_stocks, bg="green", fg="white")
        buy_button.grid(row=0, column=2, padx=5, pady=5)

        sell_button = tk.Button(control_frame, text="Sell", command=self.sell_stocks, bg="red", fg="white")
        sell_button.grid(row=0, column=3, padx=5, pady=5)

        # 停止按钮
        stop_button = tk.Button(window, text="Stop", command=self.stop_simulation, bg="gray", fg="white")
        stop_button.pack(pady=10)

        # 启动播放线程
        threading.Thread(target=self.play_music_with_chart_update, args=(ax, canvas)).start()

        window.protocol("WM_DELETE_WINDOW", self.stop_simulation)
        window.mainloop()

    def play_music_with_chart_update(self, ax, canvas):
        """
        实时更新价格曲线，并根据精确价格变化播放音符。
        """
        while self.index < len(self.prices) - 1 and not self.stop_thread:
            current_price = self.prices[self.index]
            next_price = self.prices[self.index + 1]

            # 更新曲线图
            ax.set_xlim(0, self.index + 2)
            ax.set_ylim(min(self.prices[:self.index + 2]) * 0.95, max(self.prices[:self.index + 2]) * 1.05)
            self.line.set_data(range(self.index + 2), self.prices[:self.index + 2])
            canvas.draw()

            # 根据价格变化播放音符
            self.sound_manager.play_based_on_price(current_price, next_price)

            # 更新价格显示
            self.price_label.config(text=f"Current Price: ${next_price:.2f}")

            # 更新用户资金和仓位信息
            self.update_player_info(next_price)

            self.index += 1
            time.sleep(1)  # 每秒更新一次价格


    def buy_stocks(self):
        """
        处理买入操作，更新用户资金和仓位。
        """
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            current_price = self.prices[self.index]
            total_cost = current_price * quantity
            if self.market.buy_stock(current_price, quantity):
                messagebox.showinfo("Success", f"Bought {quantity} stocks at ${current_price:.2f}.")
            else:
                messagebox.showerror("Error", f"Not enough money to buy {quantity} stocks.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def sell_stocks(self):
        """
        处理卖出操作，更新用户资金和仓位。
        """
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            current_price = self.prices[self.index]
            if self.market.sell_stock(current_price, quantity):
                messagebox.showinfo("Success", f"Sold {quantity} stocks at ${current_price:.2f}.")
            else:
                messagebox.showerror("Error", f"Not enough stocks to sell {quantity}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_player_info(self, current_price):
        """
        更新用户资金、仓位和总价值显示。
        """
        self.money_label.config(text=f"Money: ${self.market.player_money:.2f}")
        self.stock_label.config(text=f"Stocks: {self.market.player_stocks}")
        total_value = self.calculate_total_value(current_price)
        self.total_label.config(text=f"Total Value: ${total_value:.2f}")

    def calculate_total_value(self, current_price=None):
        """
        计算总资金（现有资金 + 仓位价值）。
        """
        if current_price is None:
            current_price = self.prices[self.index]
        return self.market.player_money + self.market.player_stocks * current_price

    def stop_simulation(self):
        """
        停止价格更新和声音播放。
        """
        self.stop_thread = True
        print("Simulation Stopped")
