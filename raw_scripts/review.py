import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.types import Integer
import os
from dotenv import load_dotenv

# Cấu hình
file_path = Path(r"E:\Download\Data_AE_Test\Data\Yelp JSON\yelp_academic_dataset_review.json")
batch_size = 200_000
review_data_batch = []
batch_idx = 0

pd.set_option('display.max_columns', None)

# Load biến môi trường PostgreSQL
load_dotenv(override=True)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = "localhost"

# Tạo engine PostgreSQL
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Định nghĩa schema ép kiểu
dtype_mapping = {
    'stars': Integer,
    'useful': Integer,
    'funny': Integer,
    'cool': Integer
}

# Đọc và batch insert
with file_path.open(encoding='utf-8') as f:
    for i, line in enumerate(tqdm(f, desc="Reading Yelp reviews")):
        data = json.loads(line)
        flat = {
            'review_id': data.get('review_id'),
            'user_id': data.get('user_id'),
            'business_id': data.get('business_id'),
            'stars': data.get('stars'),
            'useful': data.get('useful'),
            'funny': data.get('funny'),
            'cool': data.get('cool'),
            'text': data.get('text'),
            'date': data.get('date')
        }
        review_data_batch.append(flat)

        if (i + 1) % batch_size == 0:
            df_batch = pd.DataFrame(review_data_batch)
            df_batch.to_sql(
                "all_yelp_review",
                engine,
                if_exists="replace" if batch_idx == 0 else "append",
                index=False,
                dtype=dtype_mapping
            )
            print(f"Inserted batch {batch_idx}")
            batch_idx += 1
            review_data_batch = []

# Ghi phần dư cuối cùng nếu còn
if review_data_batch:
    df_batch = pd.DataFrame(review_data_batch)
    df_batch.to_sql(
        "all_yelp_review",
        engine,
        if_exists="replace" if batch_idx == 0 else "append",
        index=False,
        dtype=dtype_mapping
    )
    print(f"Inserted final batch {batch_idx}")
