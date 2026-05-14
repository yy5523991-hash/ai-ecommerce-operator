#!/usr/bin/env python3
"""Diagnose ecommerce note/product metrics and output the next corrections."""

from __future__ import annotations

import argparse


def rate(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def pct(value: float) -> str:
    return f"{value:.1%}"


def diagnose(args: argparse.Namespace) -> tuple[str, list[str]]:
    ctr = rate(args.clicks, args.exposure)
    save_rate = rate(args.saves, args.clicks)
    cart_rate = rate(args.carts, args.clicks)
    order_rate = rate(args.orders, args.clicks)
    refund_rate = rate(args.refunds, args.orders)

    if args.exposure < 300:
        return (
            f"曝光不足：当前曝光 {args.exposure}",
            [
                "重写标题，把核心词放前 18 个字：人群 + 场景 + 类目词 + 结果。",
                "封面加具体痛点，不写泛词：把「好用收纳」改成「桌面线乱的人先看这个」。",
                "换 3 个搜索词发布 3 篇同款不同角度笔记。",
            ],
        )
    if ctr < 0.02:
        return (
            f"点击率低：当前点击率 {pct(ctr)}",
            [
                "封面改成前后对比，左边乱、右边整齐，中间放产品。",
                "标题加入结果词：省空间、不打孔、显整齐、出差不乱。",
                "首图文字控制在 8-14 个字，只保留一个明确承诺。",
            ],
        )
    if save_rate < 0.08:
        return (
            f"收藏率低：当前收藏率 {pct(save_rate)}",
            [
                "补尺寸、材质、适合/不适合，降低用户判断成本。",
                "增加第 4-5 张细节图，拍厚度、容量、安装步骤。",
                "正文加入可复制清单：买前先量长宽高，超过 XX cm 选大号。",
            ],
        )
    if cart_rate < 0.02:
        return (
            f"加购率低：当前加购率 {pct(cart_rate)}",
            [
                "详情页增加 SKU 决策表：小号适合谁，大号适合谁。",
                "设置 3-10 元券或 2 件套，让用户有立即行动理由。",
                "把店铺置顶商品改成笔记同款，减少跳转后的找货成本。",
            ],
        )
    if order_rate < 0.01:
        return (
            f"成交率低：当前成交率 {pct(order_rate)}",
            [
                "补客服自动回复：尺寸、发货、退换、适合场景。",
                "主图第 7 张加入售后承诺和购买建议。",
                "测试一个套装价和一个单件价，保留转化更高的。",
            ],
        )
    if refund_rate > 0.08:
        return (
            f"退款率高：当前退款率 {pct(refund_rate)}",
            [
                "检查差评关键词，若出现异味、断裂、尺寸不准，立刻停推。",
                "详情页提前写清尺寸误差、承重边界、适用/不适用场景。",
                "更换供应商或只保留低投诉 SKU。",
            ],
        )
    return (
        "数据健康",
        [
            "把当前笔记结构复制到同类产品，连续发 3 篇。",
            "做套装或颜色扩展，提高客单价。",
            "找供应商谈阶梯价或运费优惠。",
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exposure", type=float, required=True)
    parser.add_argument("--clicks", type=float, required=True)
    parser.add_argument("--saves", type=float, default=0)
    parser.add_argument("--carts", type=float, default=0)
    parser.add_argument("--orders", type=float, default=0)
    parser.add_argument("--refunds", type=float, default=0)
    args = parser.parse_args()

    bottleneck, actions = diagnose(args)
    print(f"瓶颈：{bottleneck}")
    print("今日只改这3件事：")
    for index, action in enumerate(actions, 1):
        print(f"{index}. {action}")


if __name__ == "__main__":
    main()
