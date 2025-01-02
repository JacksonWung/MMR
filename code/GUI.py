import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time
import threading
import os
import pandas as pd
import sys


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
        self.window = tk.Tk()
        self.window.title("Stock Market Simulator")
        self.window.geometry("1200x800")
        self.window.configure(bg="#f0f8ff")  # Set background color

        # Start initial background music
        self.sound_manager.play_drum("normal")

        # Top information section
        top_frame = tk.Frame(self.window, bg="#d9edf7", relief="raised", bd=2)
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        self.money_label = tk.Label(top_frame, text=f"Money: ${self.market.player_money:.2f}", font=("Arial", 14),
                                    bg="#d9edf7")
        self.money_label.pack(side="left", padx=20, pady=10)

        self.stock_label = tk.Label(top_frame, text=f"Stocks: {self.market.player_stocks}", font=("Arial", 14),
                                    bg="#d9edf7")
        self.stock_label.pack(side="left", padx=20, pady=10)

        self.total_label = tk.Label(top_frame, text=f"Total Value: ${self.calculate_total_value():.2f}",
                                    font=("Arial", 14), bg="#d9edf7")
        self.total_label.pack(side="left", padx=20, pady=10)

        # Chart section
        center_frame = tk.Frame(self.window, bg="#f0f8ff")
        center_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_title("Stock Price Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        self.line, = ax.plot([], [], color="blue")

        # Set background color
        fig.patch.set_facecolor("#f0f8ff")
        ax.set_facecolor("#e6f7ff")

        canvas = FigureCanvasTkAgg(fig, master=center_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.price_label = tk.Label(center_frame, text="Current Price: $0.00", font=("Verdana", 16, "bold"),
                                    fg="#0056b3", bg="#f0f8ff")
        self.price_label.pack(pady=10)

        # Control buttons
        bottom_frame = tk.Frame(self.window, bg="#d9edf7", relief="raised", bd=2)
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        control_frame = tk.Frame(bottom_frame, bg="#d9edf7")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Quantity:", bg="#d9edf7", font=("Arial", 12)).grid(row=0, column=0, padx=5,
                                                                                         pady=5)
        self.quantity_entry = tk.Entry(control_frame, width=10)
        self.quantity_entry.grid(row=0, column=1, padx=5, pady=5)

        buy_button = tk.Button(control_frame, text="Buy", command=self.buy_stocks, bg="#28a745", fg="white",
                               font=("Helvetica", 14, "bold"))
        buy_button.grid(row=0, column=2, padx=10, pady=10)

        sell_button = tk.Button(control_frame, text="Sell", command=self.sell_stocks, bg="#dc3545", fg="white",
                                font=("Helvetica", 14, "bold"))
        sell_button.grid(row=0, column=3, padx=10, pady=10)

        quit_button = tk.Button(bottom_frame, text="Quit", command=self.quit_program, bg="black", fg="white",
                                font=("Helvetica", 12, "bold"))
        quit_button.pack(side="bottom", pady=10)

        threading.Thread(target=self.play_music_with_chart_update, args=(ax, canvas)).start()

        self.window.protocol("WM_DELETE_WINDOW", self.quit_program)
        self.window.mainloop()

    def show_feedback_window(self):
        feedback_window = tk.Toplevel()
        feedback_window.title("Feedback Form")
        feedback_window.geometry("700x800")
        feedback_window.configure(bg="#e6f7ff")

        tk.Label(
            feedback_window,
            text="We Value Your Feedback!",
            font=("Helvetica", 24, "bold"),
            bg="#e6f7ff",
            fg="#004085"
        ).pack(pady=20)

        questions = [
            ("Do you understand what to do?", "radio"),
            ("How was your experience?", "scale"),
            ("Do you understand the relationship between stock prices and music?", "radio"),
            ("How can we improve our design?", "entry"),
            ("Was the interface easy to use?", "scale"),
            ("Would you recommend this game to others?", "radio")
        ]

        vars_list = []

        def create_question(frame, question_text, var_type="entry"):
            tk.Label(frame, text=question_text, font=("Arial", 14, "bold"), bg="#f0faff").pack(anchor="w", pady=5)
            if var_type == "scale":
                var = tk.IntVar(value=4)
                scale = tk.Scale(frame, from_=1, to=7, orient=tk.HORIZONTAL, variable=var, bg="#f0faff")
                scale.pack(anchor="w", pady=5)
                return var
            elif var_type == "radio":
                var = tk.StringVar(value="Yes")
                frame_inner = tk.Frame(frame, bg="#f0faff")
                frame_inner.pack(anchor="w", pady=5)
                tk.Radiobutton(frame_inner, text="Yes", value="Yes", variable=var, bg="#f0faff").pack(side="left")
                tk.Radiobutton(frame_inner, text="No", value="No", variable=var, bg="#f0faff").pack(side="left")
                return var
            elif var_type == "entry":
                var = tk.StringVar()
                entry = tk.Entry(frame, textvariable=var, width=60)
                entry.pack(anchor="w", pady=5)
                return var

        for question, q_type in questions:
            vars_list.append(create_question(feedback_window, question, q_type))

        def submit_feedback():
            feedback_results = {f"Q{i+1}": var.get() for i, var in enumerate(vars_list)}

            file_path = "feedback.xlsx"
            df = pd.DataFrame([feedback_results])
            if os.path.exists(file_path):
                existing_df = pd.read_excel(file_path, engine="openpyxl")
                df = pd.concat([existing_df, df], ignore_index=True)
            df.to_excel(file_path, index=False, engine="openpyxl")

            messagebox.showinfo("Thank You", "Thank you for your feedback!")
            feedback_window.destroy()

            if hasattr(self, "window") and self.window:
                self.window.destroy()

            sys.exit(0)

        submit_button = tk.Button(
            feedback_window,
            text="Submit",
            command=submit_feedback,
            font=("Helvetica", 18, "bold"),
            bg="#28a745",
            fg="white",
            relief="raised",
            bd=3,
            width=20,
            height=2
        )
        submit_button.pack(side="bottom", pady=20)




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
            time.sleep(2)  # 每秒更新一次价格

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
            if not self.market.buy_stock(current_price, quantity):
                messagebox.showerror("Error", f"Not enough money to buy {quantity} stocks.")
            else:
                self.update_player_info(current_price)
                messagebox.showinfo("Buy", f"Bought 1 stock at {current_price}.", icon="info")
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
            if not self.market.sell_stock(current_price, quantity):
                messagebox.showerror("Error", f"Not enough stocks to sell {quantity}.")
            else:
                self.update_player_info(current_price)
                messagebox.showinfo("Buy", f"Bought 1 stock at {current_price}.", icon="info")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def buy_stocks_fixed(self, quantity):
        """
        Buy a fixed quantity of stocks - either 1, 5, 10, 20, 50 or 100
        """
        current_price = self.prices[self.index]
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            total_cost = current_price * quantity
            if not self.market.buy_stock(current_price, quantity):
                messagebox.showerror("Error", f"Not enough money to buy {quantity} stocks.")
            else:
                self.update_player_info(current_price)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def sell_stocks_fixed(self, quantity):
        """
        Sell a fixed quantity of stocks - either 1, 5, 10, 20, 50 or 100
        """
        current_price = self.prices[self.index]
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            if not self.market.sell_stock(current_price, quantity):
                messagebox.showerror("Error", f"Not enough stocks to sell {quantity}.")
            else:
                self.update_player_info(current_price)
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
        # 计算资产变化百分比
        initial_total = 100000.0  # 假设初始资金为 1000
        change_percent = ((total_value - initial_total) / initial_total) * 100
        # 根据资产变化播放对应的背景音乐
        if change_percent >= 2:
            new_state = "gain"
        elif change_percent <= -2:
            new_state = "loss"
        else:
            new_state = "normal"

        # 切换背景音乐
        self.sound_manager.play_drum(new_state)

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

    def quit_program(self):
        """
        安全退出程序：
        - 停止线程
        - 关闭窗口
        """
        self.stop_thread = True
        self.show_feedback_window()

    def restart_program(self):
        """
        重启程序：
        - 停止当前线程
        - 重置用户资金、仓位和价格曲线
        - 重新启动播放线程
        """
        # 停止当前线程
        if hasattr(self, "play_thread") and self.play_thread.is_alive():
            self.stop_thread = True  # 通知线程停止
            self.play_thread.join()  # 等待线程完全终止
        # 重置模拟状态
        self.market.player_money = 100000.0  # 重置初始资金
        self.market.player_stocks = 0  # 重置初始仓位
        self.index = 0  # 重置价格索引
        self.stop_thread = False  # 重置停止标志
        # 更新界面显示
        self.update_player_info(self.prices[self.index])
        self.price_label.config(text=f"Current Price: ${self.prices[self.index]:.2f}")
        # 重启播放线程
        threading.Thread(target=self.play_music_with_chart_update,
                         args=(self.line.axes, self.line.figure.canvas)).start()
        self.play_thread.start()
