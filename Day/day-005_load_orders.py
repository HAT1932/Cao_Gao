import argparse
import logging
import sqlite3
from pathlib import Path
import sys
import pandas as pd
from contextlib import closing

BASE = Path(__file__).resolve().parent.parent
DEFAULT_CSV = BASE / "clean_orders_v1.csv"
DEFAULT_DB = BASE / "data" / "ecom.db"
LOG_PATH = BASE / "day-005_load.log"

def setup_logger()->logging.Logger:
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - [%(levelname)s] %(name)s : %(lineno)d : %(message)s",
        datefmt = "%H:%M:%S",
        handlers =[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_PATH , encoding = "utf-8"),
        ],
    )
    return logging.getLogger("load_orders")

def load(csv_path:Path,db_path:Path,table:str)->None:
    log = logging.getLogger("load_orders")
    log.info("读入 CSV: %s", csv_path)
    df = pd.read_csv(csv_path,encoding = "utf-8-sig")
    log.info("shape = %s , column =%s",df.shape , list(df.columns))

    db_path.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(db_path) as con:
        df.to_sql(table,con,if_exists = "replace",index = False)
    log.info("写入成功：%s -> 表 %s (if_exists = replace) ",db_path,table)

def verify(db_path:Path , table:str) ->int:
    with closing (sqlite3.connect(db_path)) as con:
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        dmin,dmax,ndays = con.execute(f"SELECT MIN(order_date), MAX(order_date), COUNT(DISTINCT order_date) FROM {table}").fetchone()
        total = con.execute(f"SELECT ROUND(SUM(AMOUNT),2) FROM {table}").fetchone()[0]
        status = con.execute(
            f"SELECT status,COUNT(*) FROM {table} GROUP BY  status ORDER BY 2 DESC").fetchall()
        ddl = con.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name =?",(table,)).fetchone()[0]

    bad = []
    if n!=60:
        bad.append(f"行数{n} !=6=")
    if abs(total - 44782.99) > 0.01:
        bad.append(f"")
    if ndays != 23:
        bad.append(f"")
    if bad :
        print("" + ";".join(bad))
        return 1
    
    print("\n表结构（to_sql自动生成，注意：没有主键，没有约束）：")
    print(ddl)
    print("\n校验")
    print(f"  行数  ={n}    (期望60)")
    print(f"  日期范围 = {dmin} ~ {dmax}，共 {ndays} 天")
    print(f"  金额合计 = {total}   （期望 44782.99）")
    print("  状态分布 = " + ",".join(f"{s}={c}"for s,c in status))
    return 0 if n ==60 else 1

def main()->int:
    parser = argparse.ArgumentParser(description = "订单 CSV——>SQLite（幂等）")
    parser.add_argument("--csv",default = str(DEFAULT_CSV),help="输入CSV")
    parser.add_argument("--db",default=str(DEFAULT_DB),help="输出.db文件")
    parser.add_argument("--table",default="orders",help="输出表名")
    args = parser.parse_args()

    setup_logger()
    load(Path(args.csv),Path(args.db),args.table)
    return verify(Path(args.db),args.table)

if __name__ == "__main__":
    raise SystemExit(main())