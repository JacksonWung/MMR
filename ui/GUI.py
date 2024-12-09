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

    def show_instruction_window(self):
        """
        Display a multi-step instruction guide for new users.
        """

        root = tk.Tk()
        root.withdraw()

        instructions = [
            "Welcome to the Stock Market Simulator!\n\n"
            "This game simulates real-world stock trading combined with a musical experience. "
            "Stock price movements are represented by musical pitches: higher prices lead to higher pitches, "
            "and lower prices lead to lower pitches. Your objective is to trade stocks while enjoying the musical dynamics.",

            "Stock Market Basics:\n\n"
            "1. To profit, buy stocks at a low price and sell them at a higher price.\n"
            "2. Larger investments may yield higher profits but come with greater risks.\n"
            "3. Monitor the stock price graph and musical cues to make strategic decisions.\n"
            "4. Remember: A good trader always balances risks and rewards.",
        
            "How to Play:\n\n"
            "1. You start with $100,000 in virtual money.\n"
            "2. Stock prices and your portfolio details are displayed in real-time.\n"
            "3. Input the number of shares to trade and click the Buy or Sell button.\n"
            "   Alternatively, use shortcut buttons for quick trades.\n"
            "4. Restrictions:\n"
            "   - You can only buy stocks if you have enough funds.\n"
            "   - You can only sell stocks if you have shares in your portfolio.\n"
            "5. Aim to maximize your total value by trading wisely.",
        ]

        def next_instruction(index=0):
            if index < len(instructions):
                instruction_window = tk.Toplevel()
                instruction_window.title("Instruction")
                instruction_window.geometry("600x400")
        


                # Add content
                tk.Label(
                    instruction_window,
                    text=instructions[index],
                    wraplength=550,
                    justify="left",
                    font=("Arial", 12)
                ).pack(pady=20)
        
                # Add buttons
                if index < len(instructions) - 1:
                    tk.Button(
                        instruction_window,
                        text="Next",
                        command=lambda: [instruction_window.destroy(), next_instruction(index + 1)]
                    ).pack(pady=10)
                else:
                    tk.Button(
                        instruction_window,
                        text="Start Game",
                        command=lambda: [instruction_window.destroy(), self.create_main_window()]
                    ).pack(pady=10)
            else:
                self.destroy()

                

        next_instruction()
        root.mainloop()
    
    def create_main_window(self):
        window = tk.Tk()
        window.title("Stock Market Simulator")
        window.geometry("1200x800")
        # Start initial background music
        self.sound_manager.play_drum("normal")
        # Line plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_title("Stock Price Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        self.line, = ax.plot([], [], color="blue")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack()
        # Player funds and stock info
        self.money_label = tk.Label(window, text=f"Money: ${self.market.player_money:.2f}", font=("Arial", 12))
        self.money_label.pack()
        self.stock_label = tk.Label(window, text=f"Stocks: {self.market.player_stocks}", font=("Arial", 12))
        self.stock_label.pack()
        self.total_label = tk.Label(window, text=f"Total Value: ${self.calculate_total_value():.2f}",
                                    font=("Arial", 12))
        self.total_label.pack()
        # Current price display
        self.price_label = tk.Label(window, text="Current Price: $0.00", font=("Arial", 12))
        self.price_label.pack()
        # Buy and sell manually
        control_frame = tk.Frame(window)
        control_frame.pack(pady=10)
        tk.Label(control_frame, text="Quantity:").grid(row=0, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(control_frame, width=10)
        self.quantity_entry.grid(row=0, column=1, padx=5, pady=5)
        buy_button = tk.Button(control_frame, text="Buy", command=self.buy_stocks, bg="green", fg="white")
        buy_button.grid(row=0, column=2, padx=5, pady=5)
        sell_button = tk.Button(control_frame, text="Sell", command=self.sell_stocks, bg="red", fg="white")
        sell_button.grid(row=0, column=3, padx=5, pady=5)
        # Buy and Sell Predefined Quantities
        quantity_frame = tk.Frame(window)
        quantity_frame.pack(pady=10)
        # Buy Buttons
        buy_label = tk.Label(quantity_frame, text="Buy:")
        buy_label.grid(row=0, column=0, padx=0, pady=0)
        for i, amount in enumerate([1, 5, 10, 20, 50, 100]):
            btn = tk.Button(quantity_frame, text=f"{amount}", command=lambda a=amount: self.buy_stocks_fixed(a), bg="green",
                            fg="white", height=1, width=3)
            btn.grid(row=0, column=i + 1, padx=0, pady=0)
        # Sell Buttons
        sell_label = tk.Label(quantity_frame, text="Sell:")
        sell_label.grid(row=1, column=0, padx=0, pady=0)
        for i, amount in enumerate([1, 5, 10, 20, 50, 100]):
            btn = tk.Button(quantity_frame, text=f"{amount}", command=lambda a=amount: self.sell_stocks_fixed(a), bg="red",
                            fg="white", height=1, width=3)
            btn.grid(row=1, column=i + 1, padx=0, pady=0)
        # Control buttons
        control_frame2 = tk.Frame(window)
        control_frame2.pack(pady=10)
        stop_button = tk.Button(control_frame2, text="Stop", command=self.stop_simulation, bg="gray", fg="white")
        stop_button.grid(row=0, column=0, padx=5, pady=5)
        restart_button = tk.Button(control_frame2, text="Restart", command=self.restart_program, bg="blue", fg="white")
        restart_button.grid(row=0, column=1, padx=5, pady=5)
        quit_button = tk.Button(control_frame2, text="Quit", command=self.quit_program, bg="black", fg="white")
        quit_button.grid(row=0, column=2, padx=5, pady=5)
        # Start the simulation thread
        threading.Thread(target=self.play_music_with_chart_update, args=(ax, canvas)).start()
        window.protocol("WM_DELETE_WINDOW", self.quit_program)
        window.mainloop()

    def show_feedback_window(self):
        """
        Display a feedback form to collect user experience.
        """

        # Create root if not already initialized
        global root
        root = tk.Tk()
        root.withdraw()

        feedback_window = tk.Toplevel()
        feedback_window.title("Feedback Form")
        feedback_window.geometry("1000x1100")

        # Create a dictionary to store feedback
        feedback_data = {}

        # Helper to create a label and input
        def create_question(frame, question_text, var_type="entry"):
            tk.Label(frame, text=question_text, font=("Arial", 12)).pack(anchor="w", pady=5)
            if var_type == "scale":
                var = tk.IntVar(value=4)
                scale = tk.Scale(frame, from_=1, to=7, orient=tk.HORIZONTAL, variable=var)
                scale.pack(anchor="w", pady=5)
                return var
            elif var_type == "radio":
                var = tk.StringVar(value="Yes")
                frame_inner = tk.Frame(frame)
                frame_inner.pack(anchor="w", pady=5)
                tk.Radiobutton(frame_inner, text="Yes", value="Yes", variable=var).pack(side="left")
                tk.Radiobutton(frame_inner, text="No", value="No", variable=var).pack(side="left")
                return var
            elif var_type == "entry":
                var = tk.StringVar()
                entry = tk.Entry(frame, textvariable=var, width=50)
                entry.pack(anchor="w", pady=5)
                return var

        # Create compulsory questions
        questions_frame = tk.Frame(feedback_window)
        questions_frame.pack(pady=10, padx=20, fill="x")

        compulsory_questions = [
            ("Do you understand what to do?", "radio"),
            ("How was your experience?", "scale"),
            ("Do you understand the relationship between stock prices and music?", "radio"),
            ("How can we improve our design?", "entry"),
            ("Was the interface easy to use?", "scale"),
            ("Would you recommend this game to others?", "radio")
        ]
        compulsory_vars = []
        for q_text, q_type in compulsory_questions:
            compulsory_vars.append(create_question(questions_frame, q_text, var_type=q_type))

        # Create optional questions
        optional_frame = tk.LabelFrame(feedback_window, text="Optional Questions", font=("Arial", 12))
        optional_frame.pack(pady=10, padx=20, fill="x")

        optional_questions = [
            ("What features did you enjoy the most?", "entry"),
            ("Any specific feedback about the music?", "entry"),
            ("Would you play this game again?", "radio"),
            ("Do you have any suggestions for new features?", "entry")
        ]
        optional_vars = []
        for q_text, q_type in optional_questions:
            optional_vars.append(create_question(optional_frame, q_text, var_type=q_type))

        # Submit feedback
        def submit_feedback():
            # Check if all compulsory questions are answered
            for var in compulsory_vars:
                if isinstance(var, tk.StringVar) and not var.get():
                    messagebox.showerror("Error", "Please answer all compulsory questions.")
                    return
                elif isinstance(var, tk.IntVar) and var.get() == 0:
                    messagebox.showerror("Error", "Please answer all compulsory questions.")
                    return

            # Collect feedback
            feedback_data.update({
                f"Q{i+1}": var.get() if isinstance(var, tk.StringVar) else var.get()
                for i, var in enumerate(compulsory_vars)
            })
            feedback_data.update({
                f"Optional Q{i+1}": var.get() if isinstance(var, tk.StringVar) else var.get()
                for i, var in enumerate(optional_vars)
            })

            # Save to Excel
            file_path = "feedback.xlsx"
            
            df = pd.DataFrame([feedback_data])
            if os.path.exists(file_path):
                existing_df = pd.read_excel(file_path)
                df = pd.concat([existing_df, df], ignore_index=True)
            df.to_excel(file_path, index=False)

            messagebox.showinfo("Thank You", "Thank you for your feedback!")
            feedback_window.destroy()
            root.quit()
            sys.exit(0)

        tk.Button(feedback_window, text="Submit", command=submit_feedback, bg="blue", fg="white").pack(pady=10)
    

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
        initial_total = 1000.0  # 假设初始资金为 1000
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
        self.market.player_money = 1000.0  # 重置初始资金
        self.market.player_stocks = 0      # 重置初始仓位
        self.index = 0                     # 重置价格索引
        self.stop_thread = False           # 重置停止标志
        # 更新界面显示
        self.update_player_info(self.prices[self.index])
        self.price_label.config(text=f"Current Price: ${self.prices[self.index]:.2f}")
        # 重启播放线程
        threading.Thread(target=self.play_music_with_chart_update, args=(self.line.axes, self.line.figure.canvas)).start()
        self.play_thread.start()