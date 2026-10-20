import argparse

parser = argparse.ArgumentParser(description="生成日订单量/客单价/退款率日报")
parser.add_argument("--input",  default="clean_orders.csv", help="输入：清洗后的订单 CSV")
parser.add_argument("--output", default="daily_report.csv", help="输出：日报 CSV")
parser.add_argument("--start",  default=None, help="只统计该日期之后，如 2024-01-01")
args = parser.parse_args()

print(args.input, args.output, args.start)