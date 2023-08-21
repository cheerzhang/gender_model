import pandas as pd

class DATA_A_SCORE:
    def __init__(self):
        pass
    def process_fe(self, df):
        # post code 4
        df['customer_postcode'] = df['customer_postcode'].str.replace('O', '0')
        df['customer_postcode'] = df['customer_postcode'].str.replace('o', '0')
        df['postcode_4'] = pd.to_numeric(df['customer_postcode'].str[0:4], errors='coerce').astype(float)
        # house number
        if df['customer_house_number'].dtype == 'object':
            df['house_number'] = df['customer_house_number'].str.extract(r'(\d+)', expand=False).astype(float)
        else:
            df['house_number'] = df['customer_house_number']
        # delivery house number
        if df['customer_delivery_house_number'].dtype == 'object':
            df['d_house_number'] = df['customer_delivery_house_number'].str.extract(r'(\d+)', expand=False).astype(float)
        else:
            df['d_house_number'] = df['customer_delivery_house_number']
        # order month
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df['order_month'] = df['created_at'].dt.month
        # features
        features = ['postcode_4', 'house_number', 'd_house_number', 'total_price_inc_vat', 'client_id', 'order_month']
        return df[features]