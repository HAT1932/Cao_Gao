"""
把你的 clean_orders_v1.csv 导入 SQLite -> ecom_real.db 的 orders 表

运行： python3 scripts/load_real.py
"""
import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "user_data" / "clean_orders_v1.csv"
DB = BASE / "data" / "ecom_real.db"

df = pd.read_csv(CSV, encoding="utf-8-sig")
print(f"读入 {len(df)} 行，列名：{list(df.columns)}")

con = sqlite3.connect(DB)
df.to_sql("orders", con, if_exists="replace", index=False)

n, = con.execute("SELECT COUNT(*) FROM orders").fetchone()
print(f"\n✅ 已写入 {DB} 的 orders 表：{n} 行")
print("\n建表语句：")
print(con.execute("SELECT sql FROM sqlite_master WHERE name='orders'").fetchone()[0])
con.close()
print("\n接下来： python3 scripts/run_queries.py sql/queries_real.sql data/ecom_real.db")
