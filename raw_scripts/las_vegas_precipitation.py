import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load biến môi trường (nếu bạn dùng file .env)

# Thông tin kết nối Postgres (điền thông tin bạn đang dùng)
load_dotenv(override=True)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = "localhost"  # Docker expose ra host

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
# Đọc file CSV
df = pd.read_csv(r"E:\Download\Data_AE_Test\Data\Climate Data\las-vegas-mccarran-intl-ap-precipitation-inch.csv")

# Kiểm tra dữ liệu đầu tiên

# Ghi vào bảng Postgres (tạo bảng mới hoặc ghi đè)
df.to_sql("all_lv_precipitation", engine, if_exists="replace", index=False)

print("✅ Done! Data precipitation has been loaded into Postgres.")
