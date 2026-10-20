# ✅ 正确：with 自动关闭，即使中途报错
import json
import csv
import argparse

with open("text.txt", "a", encoding="utf-8") as f:
    f.write("\nhello")
"""  JSON
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)   # 得到 dict，之后当普通字典用

# 写 JSON（ensure_ascii=False 才能存中文，indent 美化）
with open("out.json", "w", encoding="utf-8") as f:
    json.dump({"name": "订单报表"}, f, ensure_ascii=False, indent=2)
"""
"""
with open("report.csv","w",encoding = "utf-8-sig",newline="") as f:
    fieldnames = ["order_id","amount","status"]
    writer = csv.DictWriter (f,fieldnames = fieldnames)
    writer.writeheader()
    writer.writerow({"order_id":"A001","amount":"100","status":"已支付"})

with open("report.csv","r",encoding = "utf-8-sig") as f :
    for row in csv.DictReader(f):
        print(f"order_id:{row['order_id']},amount:{row['amount']},status:{row['status']}")
"""

"""生成JSON
x={
  "date": "2026-10-13",
  "channel": "天猫旗舰店",
  "orders": [
    {"order_id": "T1001", "user": "张三", "amount": 299.0, "status": "paid"},
    {"order_id": "T1002", "user": "李四", "amount": 1580.5, "status": "paid"},
    {"order_id": "T1003", "user": "王五", "amount": 89.9, "status": "refunded"},
    {"order_id": "T1004", "user": "赵六", "amount": 420.0, "status": "pending"},
    {"order_id": "T1005", "user": "钱七", "amount": 66.0, "status": "paid"}
  ]
}
with open ("orders.json","w",encoding = "utf-8") as f:
    json.dump(x,f,ensure_ascii=False , indent = 2)
"""
try:
    with open ("orders.json","r",encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print('默认文件不存在，请检查')
#    config={**DEFAULT_CONFIG, **user_config}
    config = {"default":"True"}
except PermissionError as e:
    print(f"文件权限错误，请检查:{e}")
    config = {"defalut":"True"}
except json.JSONDecodeError as e:
    print(f"格式坏了{e}")  
    config={}  
else:
    print("Done")

order_csv = {}
order_csv ["date"] = data.get("date",0)
order_csv ["channel"] = data.get("channel",0)
for o in data["orders"]:
    order_csv ["total_orders"] = order_csv.get("total_orders",0) + 1
    order_csv ["total_amount"] = order_csv.get("total_amount",0) + o.get("amount",0)    
    if o["status"] == "paid":
        order_csv ["paid_amount"] = order_csv.get("paid_amount",0) + o.get("amount",0)
    if o["status"] == "refunded":
        order_csv ["refund_count"] = order_csv.get("refund_count",0) + 1    
order_csv["total_amount"] = f"{order_csv.get('total_amount', 0):.2f}"
order_csv["paid_amount"] = f"{order_csv.get('paid_amount', 0):.2f}"

with open("report_2026-10-13.csv","w",encoding = "utf-8-sig",newline = "")as f:
    fieldnames = ["date","channel", "total_orders", "total_amount","paid_amount", "refund_count"]
    writer = csv.DictWriter(f,fieldnames= fieldnames)
    writer.writeheader()
    writer.writerow(order_csv)

parser = argparse.ArgumentParser(description="生成订单日报")
parser.add_argument("--input", default="data/orders.json", help="输入JSON路径")
args = parser.parse_args()
print(args.input)