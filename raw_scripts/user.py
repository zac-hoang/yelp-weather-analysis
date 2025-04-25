import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.types import Float, Integer


# Đường dẫn tới file Yelp JSON
file_path = Path(r"E:\Download\Data_AE_Test\Data\Yelp JSON\yelp_academic_dataset_user.json")

# Load biến môi trường PostgreSQL
load_dotenv(override=True)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = "localhost"  # Docker expose ra host

# Tạo engine PostgreSQL
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Mapping kiểu dữ liệu cho to_sql
dtype_mapping = {
    'review_count': Integer,
    'useful': Integer,
    'funny': Integer,
    'cool': Integer,
    'average_stars': Float,
    'compliment_hot': Integer,
    'compliment_more': Integer,
    'compliment_profile': Integer,
    'compliment_cute': Integer,
    'compliment_list': Integer,
    'compliment_note': Integer,
    'compliment_plain': Integer,
    'compliment_cool': Integer,
    'compliment_funny': Integer,
    'compliment_writer': Integer,
    'compliment_photos': Integer
}

# Batch xử lý
batch_size = 200000
user_data_batch = []
batch_idx = 0

with file_path.open(encoding='utf-8') as f:
    for i, line in enumerate(tqdm(f, desc="Loading Yelp Users")):
        data = json.loads(line)
        flat = {
            'user_id': data.get('user_id'),
            'name': data.get('name'),
            'review_count': data.get('review_count'),
            'yelping_since': data.get('yelping_since'),
            'friends': data.get('friends'),
            'useful': data.get('useful'),
            'funny': data.get('funny'),
            'cool': data.get('cool'),
            'fans': data.get('fans'),
            'elite': data.get('elite'),
            'average_stars': data.get('average_stars'),
            'compliment_hot': data.get('compliment_hot'),
            'compliment_more': data.get('compliment_more'),
            'compliment_profile': data.get('compliment_profile'),
            'compliment_cute': data.get('compliment_cute'),
            'compliment_list': data.get('compliment_list'),
            'compliment_note': data.get('compliment_note'),
            'compliment_plain': data.get('compliment_plain'),
            'compliment_cool': data.get('compliment_cool'),
            'compliment_funny': data.get('compliment_funny'),
            'compliment_writer': data.get('compliment_writer'),
            'compliment_photos': data.get('compliment_photos')
        }
        user_data_batch.append(flat)

        if (i + 1) % batch_size == 0:
            df_batch = pd.DataFrame(user_data_batch)
            df_batch.to_sql(
                "all_yelp_user",
                engine,
                if_exists="append" if batch_idx > 0 else "replace",
                index=False,
                dtype=dtype_mapping
            )
            print(f"Inserted batch {batch_idx}")
            batch_idx += 1
            user_data_batch = []

# Ghi phần còn lại
if user_data_batch:
    df_batch = pd.DataFrame(user_data_batch)
    df_batch.to_sql(
        "all_yelp_user",
        engine,
        if_exists="append" if batch_idx > 0 else "replace",
        index=False,
        dtype=dtype_mapping
    )
    print(f"Inserted final batch {batch_idx}")
