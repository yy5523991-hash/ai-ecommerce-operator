#!/usr/bin/env python3
"""Generate a copy-paste ecommerce operating pack for beginner sellers."""

from __future__ import annotations

import argparse
from pathlib import Path


NICHES = [
    ("租房免打孔收纳", "免打孔收纳, 桌下抽屉, 门后挂架, 透明收纳盒", "3-18", "19.9-69", "重量<500g, 安装简单, 白/奶油/透明色, 售后低"),
    ("桌搭理线配件", "桌面理线, 线缆标签, 桌下理线槽, 洞洞板配件", "2-15", "16.9-59", "小体积, 高颜值, 适合前后对比, 可套装"),
    ("出差旅行收纳", "数据线收纳包, 证件包, 压缩收纳袋, 洗漱包", "5-25", "29-99", "防水或防泼, 多隔层, 轻便, 适合组合卖"),
    ("车内收纳清洁", "座椅缝隙盒, 车载挂钩, 后备箱收纳, 车窗清洁刷", "4-22", "29-89", "通用车型, 非复杂电子, 尺寸清晰"),
    ("手作礼物包装", "礼品袋, 贴纸包, 丝带, 手账收纳, 贺卡套装", "1-12", "19.9-79", "可组合套装, 季节性强, 视觉价值高, 复购好"),
]

TITLE_FORMULAS = [
    "人群 + 痛点 + 品类 + 结果",
    "场景 + 品类 + 核心卖点 + 规格",
    "租房党/学生党/打工人 + 类目词 + 避坑结果",
    "小户型 + 收纳神器 + 免打孔 + 风格",
    "出差旅行 + 便携 + 收纳包 + 多隔层",
    "桌搭 + 理线 + 风格 + 配件",
    "车内 + 不占空间 + 收纳/清洁 + 通用款",
    "礼物包装 + 高级感 + 套装 + 平价",
    "解决XX乱糟糟 + 一个小物 + 立刻整齐",
    "XX平替 + 高颜值 + 实用 + 小预算",
]


def build_pack(platform: str, budget: int, persona: str) -> str:
    platform_name = "小红书" if platform.lower() in {"xhs", "xiaohongshu", "小红书"} else platform
    niche_rows = "\n".join(
        f"| {name} | {keywords} | {cost} RMB | {price} RMB | {standard} |"
        for name, keywords, cost, price, standard in NICHES
    )
    title_rows = "\n".join(f"{idx}. `{formula}`" for idx, formula in enumerate(TITLE_FORMULAS, 1))

    return f"""# {platform_name}零基础低预算电商闭环手册

适用对象：{persona}

预算假设：{budget} RMB

## 1. 平台指令

1. 选择 `{platform_name}个人店/个人可入驻店型`。
2. 准备身份证、银行卡、手机号、退货地址、可用类目资质。
3. 店名公式：`人群/场景 + 类目 + 小店感`。
4. 首批只上 3 个 SKU，用 7-14 天内容测款。
5. 禁用夸大词：`官方`、`旗舰`、`第一`、`最`、`永久`、`治疗`、`医用`。

## 2. 五个冷门高利润类目

| 类目 | 1688搜索词 | 拿货价 | 建议售价 | 上架标准 |
|---|---|---:|---:|---|
{niche_rows}

## 3. 1688选品标准

指令：

1. 只看支持一件代发、小批量、48小时发货、可退换的供应商。
2. 毛利公式：`(售价 - 成本 - 运费 - 平台费预估 - 售后缓冲) / 售价`。
3. 毛利低于 45% 直接淘汰。
4. 重量超过 1kg 且售价低于 99 RMB 的，直接淘汰。
5. 差评反复出现 `异味/断裂/掉色/漏发/尺寸不准/做工差` 的，直接淘汰。
6. 优先选择能组合成 2件/3件/套装 的产品。

## 4. SEO爆款标题公式

{title_rows}

## 5. 不露脸图文模板

标题：

`我后悔没早点买这个XX，真的把XX救回来了`

正文：

```text
之前我的【场景】一直很乱，尤其是【具体痛点】。
后来换成这个【产品】，最明显的变化是：

1. 【变化1】
2. 【变化2】
3. 【变化3】

适合：【人群/场景】
不适合：【边界条件】
尺寸/颜色：【规格】

我放在店铺了，拿不准尺寸的可以直接问我。
```

图片顺序：

1. 痛点封面
2. 使用前
3. 使用后
4. 细节
5. 使用步骤
6. 规格对比
7. 购买建议

## 6. 客服快捷话术

欢迎：`亲，欢迎来店里～这款是【产品】，适合【场景】。需要我帮你看尺寸/颜色吗？`

推荐：`如果你是【轻度需求】，建议选【规格A】；如果东西多，直接选【规格B】，更稳也更划算。`

砍价：`亲，这款现在是小店活动价，质量和售后我会把关。你可以先领【优惠券】，到手更合适。`

发货：`亲，正常【时效】内发出，发出后系统会自动同步单号。`

售后：`抱歉影响体验了。麻烦拍一下外包装和问题位置，我核实后给你安排补发/换货/退款。`

## 7. 每天1小时打卡

| 时间 | 动作 | 输出 |
|---:|---|---|
| 10分钟 | 看曝光、点击、收藏、加购、成交、退款 | 1个瓶颈 |
| 10分钟 | 搜3个关键词，保存爆款封面和标题 | 3条可抄结构 |
| 15分钟 | 在1688筛5个候选品 | 1个候选品 |
| 20分钟 | 发或写1篇图文笔记 | 1篇笔记 |
| 10分钟 | 回复客服、催未付款、处理售后 | 清空消息 |
| 5分钟 | 记录明天第一动作 | 1条待办 |

## 8. 7天迭代

Day 1：找10款，按标准淘汰。

Day 2：问供应商一件代发、授权图、发货、退换。

Day 3：上架3款。

Day 4-6：每天发1篇笔记。

Day 7：保留有点击/收藏/咨询的款，替换无反馈款。
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", default="xiaohongshu")
    parser.add_argument("--budget", type=int, default=3000)
    parser.add_argument("--persona", default="零基础、低预算、个人店、不露脸")
    parser.add_argument("--output", help="Write Markdown to this path instead of stdout")
    args = parser.parse_args()

    content = build_pack(args.platform, args.budget, args.persona)
    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
