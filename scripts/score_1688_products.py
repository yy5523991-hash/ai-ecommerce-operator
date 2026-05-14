#!/usr/bin/env python3
"""Score 1688 product candidates for beginner ecommerce testing."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


BAD_WORDS = {"异味", "掉色", "断裂", "漏发", "尺寸不准", "做工差", "客服差", "破损", "虚标"}


def to_float(value: str, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def score_row(row: dict[str, str]) -> tuple[int, str]:
    cost = to_float(row.get("cost", "0"))
    shipping = to_float(row.get("shipping", "0"))
    sale_price = to_float(row.get("sale_price", "0"))
    weight = to_float(row.get("weight_grams", "0"))
    supplier_years = to_float(row.get("supplier_years", "0"))
    monthly_sales = to_float(row.get("monthly_sales", "0"))
    rating = to_float(row.get("rating", "0"))
    ships_hours = to_float(row.get("ships_hours", "999"))
    return_policy = str(row.get("return_policy", "")).lower()
    complaints = str(row.get("complaint_keywords", ""))

    score = 0
    reasons: list[str] = []

    gross_margin = 0.0
    if sale_price > 0:
        gross_margin = (sale_price - cost - shipping - sale_price * 0.08) / sale_price

    if gross_margin >= 0.6:
        score += 25
        reasons.append("毛利优秀")
    elif gross_margin >= 0.45:
        score += 15
        reasons.append("毛利合格")
    else:
        score -= 30
        reasons.append("毛利不足")

    if weight and weight <= 500:
        score += 15
        reasons.append("轻小件")
    elif weight <= 1000:
        score += 5
        reasons.append("重量可接受")
    else:
        score -= 15
        reasons.append("偏重")

    if supplier_years >= 3:
        score += 10
        reasons.append("供应商年限较稳")

    if monthly_sales >= 500:
        score += 10
        reasons.append("销量验证")
    elif monthly_sales >= 100:
        score += 5
        reasons.append("有基础销量")

    if rating >= 4.8:
        score += 10
        reasons.append("评分高")
    elif rating and rating < 4.5:
        score -= 10
        reasons.append("评分偏低")

    if ships_hours <= 48:
        score += 10
        reasons.append("发货快")
    else:
        score -= 5
        reasons.append("发货慢")

    if "yes" in return_policy or "支持" in return_policy or "true" in return_policy:
        score += 10
        reasons.append("支持退换")
    else:
        score -= 10
        reasons.append("退换不明")

    bad_hits = [word for word in BAD_WORDS if word in complaints]
    if bad_hits:
        score -= 25
        reasons.append("差评风险:" + "/".join(bad_hits))

    score = max(0, min(100, score))
    if score >= 75:
        action = "优先测款"
    elif score >= 55:
        action = "谨慎测款"
    else:
        action = "淘汰"

    return score, f"{action}; 毛利约{gross_margin:.0%}; " + "；".join(reasons)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    input_path = Path(args.csv_path)
    output_path = Path(args.output) if args.output else input_path.with_name(input_path.stem + "_scored.csv")

    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    for extra in ["score", "decision"]:
        if extra not in fieldnames:
            fieldnames.append(extra)

    for row in rows:
        score, decision = score_row(row)
        row["score"] = str(score)
        row["decision"] = decision

    with output_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(str(output_path))


if __name__ == "__main__":
    main()
