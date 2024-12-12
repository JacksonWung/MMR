import os
import pandas as pd


class StockData:
    @staticmethod
    def load_data(file_path):
        current_dir = os.path.dirname(__file__)
        data_path = os.path.join(current_dir, '..', 'data', file_path)
        data_path = str(data_path)

        df = pd.read_csv(data_path)
        df['Close'] = df['Close'].replace({'"': '', ',': ''}, regex=True).astype(float)
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        return df

    @staticmethod
    def get_price_range(df):
        return df['Close'].min(), df['Close'].max()
