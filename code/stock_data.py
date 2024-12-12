import pandas as pd


class StockData:
    @staticmethod
    def load_data(file_path):
        df = pd.read_csv(file_path)
        df['Close'] = df['Close'].replace({'"': '', ',': ''}, regex=True).astype(float)
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        return df

    @staticmethod
    def get_price_range(df):
        return df['Close'].min(), df['Close'].max()
