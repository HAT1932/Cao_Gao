-- Day 5 验收 C：日订单量 / 日销售额 / 客单价 / 退单数 / 退款率
-- 口径与 Day 4 的 daily_report.csv 完全一致（对账 diff 必须为 0）
-- 运行：sqlite3 -box data/ecom.db ".read sql/day05_daily_report.sql"

SELECT
    order_date,
    COUNT(DISTINCT order_id)                AS 日订单量,     -- 已给你
    ROUND(SUM(amount),2)                                    AS 日销售额,     -- 提示：SUM(?), ROUND 2 位
    ROUND(SUM(amount) / COUNT(DISTINCT order_id)  ,2)  AS 客单价,       -- 提示：上一列的表达式 / 日订单量的表达式（不能引用别名）
    SUM(CASE WHEN status = '退货' THEN 1 ELSE 0 END)            AS 退单数,       -- 提示：条件聚合
    COUNT(DISTINCT order_id)                                     AS 总单数,       -- 可选：和日订单量同值
    ROUND( 1.0 *SUM(CASE WHEN status = '退货' THEN 1 ELSE 0 END) / COUNT(DISTINCT order_id) ,2) AS 退款率        -- 提示：1.0 * 退单数 / 总单数
FROM orders
GROUP BY order_date
ORDER BY order_date;