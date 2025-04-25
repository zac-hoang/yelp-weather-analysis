import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.types import JSON, Float, Integer

from raw_utils import clean_unicode_string, safe_parse_json, clean_boolean

# Đường dẫn tới file Yelp JSON
file_path = Path(r"E:\Download\Data_AE_Test\Data\Yelp JSON\yelp_academic_dataset_business.json")
pd.set_option('display.max_columns',None)

# List chứa dữ liệu restaurants
restaurant_data = []

with file_path.open(encoding='utf-8') as f:
    for line in tqdm(f):
        data = json.loads(line)
        flat = {
            'business_id': data.get('business_id'),
            'name': data.get('name'),
            'address': data.get('address'),
            'city': data.get('city'),
            'state': data.get('state'),
            'postal_code': data.get('postal_code'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'stars': data.get('stars'),
            'review_count': data.get('review_count'),
            'is_open': data.get('is_open'),
            'categories': data.get('categories'),
        }

        # Flatten attributes
        if data.get('attributes'):
            for k, v in data['attributes'].items():
                flat[f'attr_{k}'] = v

            # Flatten hours
        if data.get('hours'):
            for k, v in data['hours'].items():
                flat[f'hour_{k}'] = v

        restaurant_data.append(flat)

# Chuyển thành DataFrame
df_restaurants = pd.DataFrame(restaurant_data)

#Clean python2 string
cols_to_clean = ['attr_WiFi', 'attr_Alcohol', 'attr_RestaurantsAttire' ,'attr_NoiseLevel']
for col in cols_to_clean:
    if col in df_restaurants.columns:
        df_restaurants[col] = df_restaurants[col].apply(clean_unicode_string)

#Convert JSONB
jsonb_cols = ['attr_BusinessParking', 'attr_Ambience', 'attr_GoodForMeal']

for col in jsonb_cols:
    if col in df_restaurants.columns:
        df_restaurants[col] = df_restaurants[col].apply(safe_parse_json)

# Định nghĩa schema ép kiểu
dtype_mapping = {
    'latitude': Float,
    'longitude': Float,
    'stars': Float,
    'review_count': Integer,
    'is_open': Integer,
    'attr_BusinessParking': JSON,
    'attr_Ambience': JSON,
    'attr_GoodForMeal': JSON,
}

#Clean boolean fields
bool_cols = [
    'attr_RestaurantsDelivery','attr_BikeParking', 'attr_OutdoorSeating', 'attr_BusinessAcceptsCreditCards',
    'attr_RestaurantsTakeOut', 'attr_ByAppointmentOnly', 'attr_Caters',
    'attr_RestaurantsReservations', 'attr_GoodForKids', 'attr_CoatCheck', 'attr_DogsAllowed',
    'attr_RestaurantsTableService', 'attr_RestaurantsGoodForGroups', 'attr_WheelchairAccessible',
    'attr_HasTV', 'attr_HappyHour', 'attr_DriveThru'
]

# Làm sạch các trường boolean
for col in bool_cols:
    if col in df_restaurants.columns:
        df_restaurants[col] = df_restaurants[col].apply(clean_boolean)

# Ghi vào PostgreSQL

load_dotenv(override=True)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = "localhost"  # Docker expose ra host


# Tạo engine PostgreSQL
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

df_restaurants.to_sql(
    "all_yelp_business",
    engine,
    if_exists="replace",
    index=False,
    dtype=dtype_mapping
)