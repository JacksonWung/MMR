import tkinter as tk
from GUI import StockMarketUI


class TutorialWindow:
    """
    Handles displaying a multi-step instruction guide for new users.
    """

    def __init__(self, start_game_callback):
        """
        Initialize the TutorialWindow.

        :param start_game_callback: Function to call when the tutorial finishes.
        """
        self.start_game_callback = start_game_callback

    def show_instruction_window(self):
        """
        Display the multi-step instruction guide.
        """
        root = tk.Tk()
        root.withdraw()

        instructions = [
            "Welcome to the Stock Market Simulator!\n\n"
            "This game simulates real-world stock trading combined with a musical experience. \n"
            "Stock price movements are represented by musical pitches: higher prices lead to higher pitches, "
            "and lower prices lead to lower pitches. Your objective is to try to make as much money as possible by \n"
            "buying and selling based off the stock price movements. \n",

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
                instruction_window.geometry("680x480")
                instruction_window.configure(bg="#f0f8ff")

                # Add title label
                tk.Label(
                    instruction_window,
                    text=f"Step {index + 1}",
                    font=("Helvetica", 18, "bold"),
                    bg="#f0f8ff",
                    fg="#0056b3"
                ).pack(pady=10)

                # Add instruction content
                tk.Label(
                    instruction_window,
                    text=instructions[index],
                    wraplength=550,
                    justify="left",
                    font=("Arial", 14),
                    bg="#f0f8ff",
                    fg="#333333"
                ).pack(pady=20)

                # Button styles
                button_bg = "#007bff"
                button_fg = "white"
                button_font = ("Helvetica", 14, "bold")

                if index < len(instructions) - 1:
                    tk.Button(
                        instruction_window,
                        text="Next",
                        command=lambda: [instruction_window.destroy(), next_instruction(index + 1)],
                        bg=button_bg,
                        fg=button_fg,
                        font=button_font,
                        relief="raised",
                        bd=3,
                        width=10
                    ).pack(pady=10)
                else:
                    tk.Button(
                        instruction_window,
                        text="Start Game",
                        command=lambda: [instruction_window.destroy(), self.start_game_callback()],
                        bg=button_bg,
                        fg=button_fg,
                        font=button_font,
                        relief="raised",
                        bd=3,
                        width=15
                    ).pack(pady=10)

        next_instruction()
        root.mainloop()
