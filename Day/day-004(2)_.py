# daily_report.py
import argparse
import logging
from pathlib import Path
import pandas as pd


def resolve_path(name):
    BASE_DIR = Path(__file__).resolve().parent.parent
    input_path = BASE_DIR  / name
    print(f"input_path = {input_path}")
    return input_path



def load_orders(path):
    """读 CSV -> DataFrame"""
    
    df = pd.read_csv(path)
    print(df.head())
    return df



def calc_daily_metrics(df):
    """groupby 日期：日订单量 / 日销售额 / 客单价"""
      # 提示：as_index=False + 命名聚合 + nunique
    r = df.groupby("order_date",as_index = False).agg(
        日订单量 = ("order_id","nunique"),
        日销售额 = ("amount","sum") 
    )
    r["客单价"] = r["日销售额"] / r["日订单量"]
    return r


def calc_refund_rate(df):
    """groupby 日期：退款率 = 当日_退款数(order_id) / 当日_总数"""
    # 提示：分母为 0 的保护；口径写注释里
    temp = df.copy()    
    g = temp.groupby("order_date",as_index = False).agg(
        退单数 = ("status",lambda s: (s == "退货").sum()),
        总单数 = ("order_id","nunique")
    )
    g["退款率"] = g["退单数"] / g["总单数"].replace(0,pd.NA)
    return g
def main():
    # 1. argparse 解析参数
    # 2. logging 初始化（INFO 级别，同时写终端和文件）
    # 3. 读数据 -> 算指标 -> 合并两张小表 -> 写 CSV
    # 4. log.info 打印关键结果，print 预览 head()
    parser = argparse.ArgumentParser(description="生成日订单量/客单价/退款率日报")
    parser.add_argument("--input", default = "clean_orders_v1.csv",help = "输入：清洗后的订单 CSV")
    parser.add_argument("--output",default = "daily_report.csv",help = "输出：日报 CSV")
    parser.add_argument("--start",default = None , help="只统计该日期之后，如 2024-01-01")
    args = parser.parse_args()
    print(args.input,args.output,args.start)

    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - [%(levelname)s] %(name)s:%(lineno)d : %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("daily_report.log", encoding = "utf-8"),
        ],
    )
    log = logging.getLogger(__name__)

    try :
        csv_path = resolve_path(args.input)
        df = load_orders(csv_path)
    except FileNotFoundError :
        log.error("输入文件不存在:%s" , args.input)
        raise

    if args.start:
        df = df[df["order_date"]>= pd.to_datetime(args.start)]
    r = calc_daily_metrics(df)
    print(r.head())
    refund_rate = calc_refund_rate(df)
    print(refund_rate.head())

    m = pd.merge(r,refund_rate,how = "left", on = "order_date",indicator = True)
    print(m.head())
    m.drop(columns = ["_merge"],inplace = True)
    m.to_csv(args.output,index = False,encoding = "utf-8-sig",float_format="%.2f")


    log.info("日报开始:%s", args.input)
    log.info("读入 %s行", len(df))
    log.info("日报结束，写入:%s", args.output)
    log.warning("^^^")
    log.error("...")





if __name__ == "__main__":
    main()