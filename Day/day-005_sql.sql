-- ============================================================
-- Day 5 练习：orders 表 20 条查询（覆盖 SELECT/WHERE/ORDER BY/LIMIT + 聚合/GROUP BY/HAVING）
-- 运行方式（在 Cao_Gao 目录下）：
--     sqlite3 -box data/ecom.db ".read Day/day-005_sql.sql"
-- 规则：
--   1) 每条 SQL 必须以分号结尾
--   2) 文件里只写 SQL，不写 .mode/.headers 这类点命令（交给命令行参数）
--   3) 先自己写，写完再对照锚点（每题的「应该看到」写在注释里）
-- ============================================================

-- ---------- A 组（1-10）：SELECT / WHERE / ORDER BY / LIMIT ----------

-- Q1 取 orders 全部列，只看前 5 行
-- 应该看到：5 行，第 1 行是 ORD0000 | 2026-01-21 | 广州 | 2 | 240.44 | 正常
SELECT * FROM orders LIMIT 5 ;

-- Q2 只看 order_id、amount 两列，取前 3 行
-- 应该看到：3 行，只有两列
SELECT order_id,amount FROM orders LIMIT 3;

-- Q3 找出所有 status = '退货' 的单，看 order_id / amount
-- 应该看到：5 行；这 5 行的金额合计 = -7150.84
SELECT order_id,amount FROM orders WHERE status = '退货';

-- Q4 找出 amount > 1000 的单，按 amount 从大到小排
-- 应该看到：20 行，第一行金额 1990.40
SELECT * FROM orders WHERE amount > 1000 ORDER BY amount DESC;

-- Q5 找出 city = '杭州' 的单，按 order_date 从早到晚排
-- 应该看到：8 行
SELECT * FROM orders WHERE city = '杭州' ORDER BY order_date ASC;

-- Q6 找出 quantity >= 5 并且 amount > 500 的单
-- 应该看到：5 行
SELECT * FROM orders WHERE quantity >=5 AND amount >500;

-- Q7 找出金额最大的 3 单（金额最大的排最前）
-- 应该看到：1990.40 → 1938.04 → 1846.42
SELECT * FROM orders ORDER BY amount DESC LIMIT 3;

-- Q8 找出 amount 为负数的单
-- 应该看到：5 行（提示：这些单的 status 是什么？跟 Q3 对比一下）
SELECT * FROM orders WHERE amount < 0;

-- Q9 找出 city 不是 '北京' 的单
-- 应该看到：42 行（提示：!= 遇上 NULL 会漏行，这题先不管，Day 6 复习）
SELECT * FROM orders WHERE city != '北京' AND city IS NOT NULL AND city is NOT '未知';  

-- Q10 找出 order_date 在 '2026-01-10' 到 '2026-01-15' 之间的单
-- 应该看到：9 行（提示：日期在库里是 TEXT，ISO 格式可以直接比较）
SELECT * FROM orders WHERE order_date BETWEEN '2026-01-10' AND '2026-01-15';

-- ---------- B 组（11-20）：聚合 / GROUP BY / HAVING ----------

-- Q11 一行查出：总行数、不同订单数、不同城市数
-- 应该看到：60 | 60 | 6
SELECT COUNT(*),COUNT(DISTINCT order_id),COUNT(DISTINCT city) FROM orders;

-- Q12 一行查出：总销售额、平均单笔金额、最大金额、最小金额（金额保留 2 位）
-- 应该看到：44782.99 | 746.38 | 1990.40 | -1998.58
SELECT ROUND(SUM(amount),2),ROUND(AVG(amount),2),ROUND(MAX(amount),2),ROUND(min(amount),2) FROM orders;

-- Q13 按城市汇总：每个城市的单量、销售额合计、平均金额，按销售额从大到小
-- 应该看到：6 行；第 1 行 北京 | 18 | 12220.94 | 678.94
SELECT city,COUNT(*)as city_quantity,ROUND(SUM(amount),2) as SUM_amount,ROUND(AVG(amount),2) FROM orders GROUP BY city ORDER BY SUM(amount) DESC;

-- Q14 按 status 统计单量，只保留单量 >= 5 的状态
-- 应该看到：2 行（正常 48、退货 5）
SELECT status,COUNT(*) FROM orders GROUP BY status HAVING COUNT(*) >=5;

-- Q15 按 order_date 统计每天的订单量，按日期从早到晚
-- 应该看到：23 行（数据只覆盖 23 天，不是 25 天）
SELECT order_date,COUNT(*) FROM orders GROUP BY order_date ORDER BY order_date ASC;

-- Q16 只保留「日订单量 >= 4」的日期
-- 应该看到：6 行
SELECT order_date , COUNT(*) FROM orders GROUP BY order_date HAVING COUNT(*)>=4;

-- Q17 每个城市的客单价（客单价 = 销售额 / 订单数），保留 2 位，从高到低
-- 应该看到：6 行；第 1 行 未知 | 1069.10（提示：分母用 COUNT(DISTINCT order_id)）
SELECT city, ROUND(SUM(amount) / COUNT(DISTINCT order_id) ,2) as KeDanJia FROM orders GROUP BY city ORDER BY KeDanJia DESC;

-- Q18 按 status 汇总：单量、金额合计、平均金额
-- 应该看到：4 行；第 1 行 正常 | 48 | 46187.18 | 962.23
SELECT status,COUNT(*),ROUND(SUM(amount),2),ROUND(AVG(amount),2) FROM orders GROUP BY status;

-- Q19 只看 status = '正常' 的单，按城市算销售额，取前 3 名
-- 应该看到：北京 13766.80 → 未知 8800.96 → 上海 7488.88
SELECT city, SUM(amount) FROM orders WHERE status = '正常' GROUP BY city ORDER BY SUM(amount) DESC LIMIT 3 ;

-- Q20 每个城市的退款率（退款率 = 退货单数 / 总单数），保留 4 位，只保留总单数 >= 5 的城市
-- 应该看到：6 行；杭州 0.2500 最高，北京 0.1111，上海 0.0909，其余 0
-- 提示：需要同时用到条件聚合（数「有多少个 status='退货'」）和 HAVING
SELECT 
    city,
    SUM(CASE WHEN status = '退货' THEN 1 ELSE 0 END) AS r_amount,
    COUNT(DISTINCT order_id) AS total,
    ROUND(1.0 * SUM(CASE WHEN status = '退货'THEN 1 ELSE 0 END)/ COUNT(DISTINCT order_id),4) AS Rate 
FROM orders 
GROUP BY city 
HAVING COUNT(DISTINCT order_id)>=5 
ORDER BY rate DESC;

