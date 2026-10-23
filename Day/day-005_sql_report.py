"""
Day 5 / 任务 5 对账：SQL 版日报 vs pandas 版 daily_report.csv

在 Cao_Gao 目录下运行：
    .\.venv\Scripts\python.exe Day\day-005_sql_report.py
"""

import argparse
import sqlite3
import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
TOL = 0.01                                   # 浮点比较容差
COLS = ["日订单量", "日销售额", "客单价", "退单数", "退款率"]


def main() -> int:
    ap = argparse.ArgumentParser(description="SQL 日报与 pandas 日报逐行对账")
    ap.add_argument("--sql", default=str(BASE / "sql" / "day05_daily_report.sql"))
    ap.add_argument("--db", default=str(BASE / "data" / "ecom.db"))
    ap.add_argument("--expect", default=str(BASE / "daily_report.csv"))
    ap.add_argument("--out", default=str(BASE / "daily_report_from_sql.csv"))
    args = ap.parse_args()

    query = Path(args.sql).read_text(encoding="utf-8")
    with sqlite3.connect(args.db) as con:
        df_sql = pd.read_sql_query(query, con)
    df_pd = pd.read_csv(args.expect, encoding="utf-8-sig")

    missing = [c for c in ["order_date", *COLS] if c not in df_sql.columns]
    if missing:
        print(f"❌ SQL 结果缺列：{missing}")
        print(f"   实际列：{list(df_sql.columns)}")
        return 1

    df_sql = df_sql.sort_values("order_date").reset_index(drop=True)
    df_pd = df_pd.sort_values("order_date").reset_index(drop=True)
    print(f"SQL 版  ：{len(df_sql)} 行 / {len(df_sql.columns)} 列")
    print(f"pandas 版：{len(df_pd)} 行 / {len(df_pd.columns)} 列")

    m = df_sql.merge(df_pd, on="order_date", how="outer",
                     suffixes=("_sql", "_pd"), indicator=True)
    vc = m["_merge"].value_counts()
    print(f"\n合并对账：两边都有={int(vc.get('both', 0))}，"
          f"只 SQL 有={int(vc.get('left_only', 0))}，只 pandas 有={int(vc.get('right_only', 0))}")

    bad_rows = 0
    for c in COLS:
        a, b = m[f"{c}_sql"], m[f"{c}_pd"]
        if c in ("日订单量", "退单数"):
            diff = a.fillna(-1) != b.fillna(-1)              # 计数必须完全相等
        else:
            diff = (a.fillna(-9e9) - b.fillna(-9e9)).abs() > TOL  # 金额允许 0.01 误差
        n = int(diff.sum())
        bad_rows += n
        print(f"  {c:<5} 不一致行数 = {n}")
        if n:
            print(m.loc[diff, ["order_date", f"{c}_sql", f"{c}_pd"]].to_string(index=False))

    print("\n总计校验：")
    ts, tp = df_sql["日订单量"].sum(), df_pd["日订单量"].sum()
    ss, sp = df_sql["日销售额"].sum(), df_pd["日销售额"].sum()
    print(f"  订单量合计 SQL={ts} / pandas={tp}")
    print(f"  销售额合计 SQL={ss:.2f} / pandas={sp:.2f}")
    print(f"  退款率整体 SQL={df_sql['退单数'].sum() / ts:.4f} / pandas={df_pd['退单数'].sum() / tp:.4f}")

    ok = bad_rows == 0 and len(df_sql) == len(df_pd) and int(vc.get("both", 0)) == len(df_pd)
    print("\n" + ("✅ PASS：SQL 版与 pandas 版逐行一致" if ok
                  else "❌ FAIL：存在差异，按上面的行定位问题"))
    if ok:
        df_sql.to_csv(args.out, index=False, encoding="utf-8-sig", float_format="%.2f")
        print(f"已写出 SQL 版日报：{args.out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())