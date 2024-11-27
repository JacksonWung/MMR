import pandas as pd
import numpy as np
import pygame
import tkinter as tk
from tkinter import messagebox
import threading
import time


pygame.init()
pygame.mixer.init()


NOTE_A4_SOUND = pygame.mixer.Sound("A4.wav")
NOTE_B4_SOUND = pygame.mixer.Sound("B4.wav")
NOTE_C5_SOUND = pygame.mixer.Sound("C5.wav")
NOTE_A4 = "A4"  
NOTE_B4 = "B4"  
NOTE_C5 = "C5"  


def play_sound(note):
    duration = 500  
    if note == NOTE_A4:
        NOTE_A4_SOUND.play()
    elif note == NOTE_B4:
        NOTE_B4_SOUND.play()
    elif note == NOTE_C5:
        NOTE_C5_SOUND.play()


def price_to_frequency(price, min_price, max_price):
    # Normalize the price to a frequency range
    normalized_price = (price - min_price) / (max_price - min_price)  # Normalize to [0, 1]

    # Map normalized price to piano notes (can be adjusted to your preference)
    if normalized_price < 0.33:
        return NOTE_A4  
    elif normalized_price < 0.67:
        return NOTE_B4  
    else:
        return NOTE_C5 

# Function to play the stock prices as a musical score
def play_stock_music(prices, interval, dates, min_price, max_price):
    global today
    for price, date in zip(prices, dates):
        note = price_to_frequency(price, min_price, max_price)
        play_sound(note)
        today = date.strftime("%m/%d/%Y")  # Update the global date
        time.sleep(interval)  # Wait for the specified interval before playing the next note

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

# Function to create GUI
def create_gui(buy_opportunities):
    global buy_dates
    buy_dates = {date.strftime("%m/%d/%Y"): is_good_buy for date, is_good_buy in buy_opportunities}
    
    window = tk.Tk()
    window.title("Stock Market Musical Score")

    date_label = tk.Label(window, text="Click the 'Buy' button for today:")
    date_label.pack(pady=10)

    # Update the date label to reflect today's date based on the latest price played
    global today
    today = buy_opportunities[-1][0].strftime("%m/%d/%Y")
    date_label.config(text=f"Click the 'Buy' button for {today}:")
    
    buy_button = tk.Button(window, text="Buy", command=lambda: on_buy_button_click(today))
    buy_button.pack(pady=20)

    window.mainloop()

def main():
    # Load CSV data
    df = pd.read_csv("stock_data.csv")
    
    # Clean up the 'Close' column and convert to float
    df['Close'] = df['Close'].replace({'"': '', ',': ''}, regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    # Calculate dynamic min and max prices
    min_price = df['Close'].min()
    max_price = df['Close'].max()

    # Generate buy opportunities
    buy_opportunities = evaluate_buy_opportunities(df)

    # Start playing the stock music in a separate thread
    interval = 1.0  # Interval between notes in seconds
    prices = df['Close'].tolist()  # Extract closing prices
    dates = df['Date'].tolist()  # Extract corresponding dates
    music_thread = threading.Thread(target=play_stock_music, args=(prices, interval, dates, min_price, max_price))
    music_thread.start()

    # Create GUI
    create_gui(buy_opportunities)

if __name__ == "__main__":
    main()
