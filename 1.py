"""
def reverseWords(input):

    # 通过空格将字符串分隔，把各个单词分隔为列表
    inputWords = input.split(" ")

    # inputWords[-1::-1] 三个参数说明：
    # 第一个参数 -1 表示从最后一个元素开始
    # 第二个参数为空，表示移动到列表开头
    # 第三个参数 -1 表示逆向步进（每次向左移动一个位置）
    inputWords = inputWords[-1::-1]

    # 重新用空格拼接单词
    output = ' '.join(inputWords)

    return output

if __name__ == "__main__":
    input = 'I like runoob'
    rw = reverseWords(input)
    print(rw)
"""
"""
# 1. 模拟 10 条订单数据：list 里放 dict
orders = [
    {"order_id": "A001", "user": "小明", "product": "键盘", "qty": 1, "price": 299.0, "status": "已支付", "date": "2026-10-01"},
    {"order_id": "A002", "user": "小红", "product": "鼠标", "qty": 2, "price": 89.0,  "status": "已支付", "date": "2026-10-01"},
    {"order_id": "A003", "user": "小明", "product": "显示器", "qty": 1, "price": 899.0, "status": "已支付", "date": "2026-10-02"},
    {"order_id": "A004", "user": "小刚", "product": "键盘", "qty": 1, "price": 299.0, "status": "未支付", "date": "2026-10-02"},
    {"order_id": "A005", "user": "小红", "product": "耳机", "qty": 1, "price": 199.0, "status": "已支付", "date": "2026-10-03"},
    {"order_id": "A006", "user": "小美", "product": "鼠标", "qty": 3, "price": 89.0,  "status": "已支付", "date": "2026-10-03"},
    {"order_id": "A007", "user": "小刚", "product": "显示器", "qty": 1, "price": 899.0, "status": "已支付", "date": "2026-10-04"},
    {"order_id": "A008", "user": "小明", "product": "耳机", "qty": 2, "price": 199.0, "status": "已支付", "date": "2026-10-04"},
    {"order_id": "A009", "user": "小美", "product": "键盘", "qty": 1, "price": 299.0, "status": "已取消", "date": "2026-10-05"},
    {"order_id": "A010", "user": "小红", "product": "显示器", "qty": 1, "price": 899.0, "status": "已支付", "date": "2026-10-05"},
]

# 2. 基础统计
total_orders = len(orders)
paid_orders = [o for o in orders if o["status"] == "已支付"]

total_sales = sum(o["qty"] * o["price"] for o in paid_orders)
avg_order_amount = total_sales / len(paid_orders) if paid_orders else 0

print("=" * 40)
print(f"订单总数：{total_orders}")
print(f"已支付订单数：{len(paid_orders)}")
print(f"已支付总销售额：¥{total_sales:.2f}")
print(f"已支付平均每单：¥{avg_order_amount:.2f}")

# 3. 按用户统计消费额（只统计已支付）
user_stats = {}
for o in paid_orders:
    amount = o["qty"] * o["price"]
    user_stats[o["user"]] = user_stats.get(o["user"], 0) + amount

print("\n按用户消费额（已支付）：")
for user, amount in sorted(user_stats.items(), key=lambda item: item[1], reverse=True):
    print(f"  {user}: ¥{amount:.2f}")

# 4. 按商品统计销量（只统计已支付）
product_stats = {}
for o in paid_orders:
    product_stats[o["product"]] = product_stats.get(o["product"], 0) + o["qty"]

print("\n按商品销量（已支付）：")
for product, qty in sorted(product_stats.items(), key=lambda item: item[1], reverse=True):
    print(f"  {product}: {qty} 件")

# 5. 按订单状态统计订单数
status_stats = {}
for o in orders:
    status_stats[o["status"]] = status_stats.get(o["status"], 0) + 1

print("\n订单状态统计：")
for status, count in status_stats.items():
    print(f"  {status}: {count} 单")

# 6. 最大单笔已支付订单
if paid_orders:
    max_order = max(paid_orders, key=lambda o: o["qty"] * o["price"])
    max_amount = max_order["qty"] * max_order["price"]
    print(f"\n最大单笔已支付订单：{max_order['order_id']}，"
          f"用户 {max_order['user']}，金额 ¥{max_amount:.2f}")
"""

records = [
    {"name": "张三", "class": "一班", "subject": "数学", "score": 92, "date": "2026-10-01"},
    {"name": "李四", "class": "一班", "subject": "语文", "score": 85, "date": "2026-10-01"},
    {"name": "王五", "class": "二班", "subject": "数学", "score": 78, "date": "2026-10-01"},
    {"name": "赵六", "class": "二班", "subject": "英语", "score": 88, "date": "2026-10-02"},
    {"name": "张三", "class": "一班", "subject": "语文", "score": 79, "date": "2026-10-02"},
    {"name": "李四", "class": "一班", "subject": "数学", "score": 95, "date": "2026-10-02"},
    {"name": "王五", "class": "二班", "subject": "英语", "score": 91, "date": "2026-10-03"},
    {"name": "赵六", "class": "二班", "subject": "数学", "score": 82, "date": "2026-10-03"},
    {"name": "孙七", "class": "一班", "subject": "英语", "score": 76, "date": "2026-10-03"},
    {"name": "周八", "class": "二班", "subject": "语文", "score": 89, "date": "2026-10-04"},
]

print(f"总成绩数为：{len(records)}")

#筛选出所有分数 >= 90 的记录，打印学生姓名、班级、科目、分数。
records_over90=[ o for o in records if o['score'] >= 90]
print("\n超过90分:")
for o in records_over90:
    print(f"学生姓名：{o['name']} 班级：{o['class']} 科目：{o['subject']} 分数：{o['score']} 日期：{o['date']}")

#按班级分组，统计每个班的总分和平均分，并按平均分从高到低排序输出
records_class={ }
for o in records:
#    if o['class'] not in records_class:
#        records_class[o['class']] = {"total" : 0 , "count" : 0}
#    records_class.setdefault(o['class'],{"total" : 0 , "count" : 0}) 
    records_class[o['class']] = records_class.get(o['class'],{'total':0,'count':0}) 
    records_class[o['class']]['total'] = records_class[o['class']]['total'] + o['score']
    records_class[o['class']]['count'] +=  1
    # records_class = ['一班 ':{"toal":0,"count":0},
    #                  '二班' :{"toal":0,"count":0}]
print("\n按班级分组，统计每个班的总分和平均分，并按平均分从高到低排序输出:") 

for o ,stats in sorted(records_class.items(), key = lambda item:item[1]['total'] / item[1]['count'],reverse=True):
    #o = '一班'-----> '二班'
    #stats = {'total':0,'count':0}
    print(f"BanJi:{o},total:{stats['total']},avg:{records_class[o]['total']/records_class[o]['count']:.1f} ")



"""setdefault 初始化
class_stats.setdefault(cls, {"total": 0, "count": 0})
class_stats[cls]["total"] += r["score"]
class_stats[cls]["count"] += 1
"""

"""循环中 定义初始化
if cls not in class_stats:
    class_stats[cls] = {"total": 0, "count": 0}
"""

""".get 初始化 
class_stats[cls] = class_stats.get(cls, {"total": 0, "count": 0})
"""

#4.按科目分组，统计每个科目的最高分，并输出科目和最高分。
records_subject={ }
#用推导式初始化
#records_subject={key['subject'] : key['score']  for key in records if key['subject'] not in records_subject}
records_subject={key['subject'] : key['score']  for key in records if key['subject'] not in records_subject}
#  records_subject =  {"YinYu":2, "shuxue":3}
for o in records:
    if o['score'] > records_subject[o['subject']]:
        records_subject[o['subject']] = o['score']
print("\n按科目分组，统计每个科目的最高分，并输出科目和最高分。")
for sub , score in sorted( records_subject.items(), key = lambda item:item[1],reverse = True):
    print(f"科目：{sub}最高分：{score}")

#找出所有记录中分数最高的那条记录，打印完整信息（姓名、班级、科目、分数、日期）。
records_max = {}
for o in records:
    if o['score'] > records_max.get('score',0):
        records_max = o
print("\n找出所有记录中分数最高的那条记录，打印完整信息（姓名、班级、科目、分数、日期）。")
print(f"学生姓名：{records_max['name']} 班级：{records_max['class']} 科目：{records_max['subject']} 分数：{records_max['score']} 日期：{records_max['date']}")        

#（可选）按日期分组，统计每天有多少条考试记录。
records_date = {}
#ewcords_date = [{'date':1,'count':1} , {'date':2,'count':2}] 
for i in records:
    records_date[i['date']] = records_date.get(i['date'],0) + 1
print("\n（可选）按日期分组，统计每天有多少条考试记录。")
for date , conunt in records_date.items():
    print(f"date:{date},count:{conunt} ") 
