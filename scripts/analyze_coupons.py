#!/usr/bin/env python3
"""
麦当劳优惠券分析脚本
分析优惠券信息并生成Markdown表格
"""

import json
import sys
from datetime import datetime, date
from typing import Dict, List, Any


def parse_date(date_str: str) -> date:
    """解析日期字符串"""
    try:
        # 尝试多种日期格式
        formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None
    except:
        return None


def categorize_coupons(coupons_data: List[Dict]) -> Dict[str, List[Dict]]:
    """分类优惠券"""
    today = date.today()

    today_coupons = []
    future_coupons = []
    expired_coupons = []

    for coupon in coupons_data:
        # 提取有效期信息
        valid_from = coupon.get("validFrom")
        valid_to = coupon.get("validTo")
        effective_date = coupon.get("effectiveDate")

        start_date = None
        end_date = None

        # 尝试解析开始日期
        if valid_from:
            start_date = parse_date(valid_from)
        elif effective_date:
            start_date = parse_date(effective_date)

        # 尝试解析结束日期
        if valid_to:
            end_date = parse_date(valid_to)

        # 分类
        if start_date and end_date:
            if start_date <= today <= end_date:
                today_coupons.append(coupon)
            elif today < start_date:
                future_coupons.append(coupon)
            else:
                expired_coupons.append(coupon)
        elif start_date:
            if start_date <= today:
                today_coupons.append(coupon)
            else:
                future_coupons.append(coupon)
        else:
            # 没有日期信息，默认为今天可用
            today_coupons.append(coupon)

    return {
        "today": today_coupons,
        "future": future_coupons,
        "expired": expired_coupons,
    }


def extract_coupon_info(coupon: Dict) -> Dict[str, Any]:
    """提取优惠券关键信息"""
    name = coupon.get("name", coupon.get("couponName", "未知优惠券"))
    description = coupon.get("description", coupon.get("couponDesc", ""))

    # 提取可购买物品
    items = []
    if "适用产品" in description:
        items = [
            desc.strip()
            for desc in description.split("适用产品:")[-1].split(";")
            if desc.strip()
        ]
    elif "可购买" in description:
        items = [
            desc.strip()
            for desc in description.split("可购买:")[-1].split("、")
            if desc.strip()
        ]

    # 提取使用条件
    conditions = []
    if "使用条件" in description:
        conditions = [
            cond.strip()
            for cond in description.split("使用条件:")[-1].split(";")
            if cond.strip()
        ]
    elif "条件" in description:
        conditions = [
            cond.strip()
            for cond in description.split("条件:")[-1].split("，")
            if cond.strip()
        ]

    # 提取有效期
    valid_from = coupon.get("validFrom", coupon.get("effectiveDate", ""))
    valid_to = coupon.get("validTo", coupon.get("expiryDate", ""))

    # 提取状态
    status = coupon.get("status", "可用")

    # 提取折扣信息
    discount = coupon.get("discount", coupon.get("discountAmount", ""))

    return {
        "name": name,
        "description": description,
        "items": items,
        "conditions": conditions,
        "valid_from": valid_from,
        "valid_to": valid_to,
        "status": status,
        "discount": discount,
    }


def generate_markdown_table(categorized_coupons: Dict[str, List[Dict]]) -> str:
    """生成Markdown表格"""
    markdown = "# 麦当劳优惠券分析报告\n\n"

    # 今天可用的优惠券
    if categorized_coupons["today"]:
        markdown += "## 1. 今天可用的优惠券\n\n"
        markdown += "| 优惠券名称 | 可购买物品 | 使用条件 | 有效期 | 状态 |\n"
        markdown += "|------------|------------|----------|--------|------|\n"

        for coupon in categorized_coupons["today"]:
            info = extract_coupon_info(coupon)

            # 格式化数据
            items_str = "、".join(info["items"][:3]) if info["items"] else "多种商品"
            if len(info["items"]) > 3:
                items_str += "等"

            conditions_str = (
                "、".join(info["conditions"][:2])
                if info["conditions"]
                else "无特殊条件"
            )
            if len(info["conditions"]) > 2:
                conditions_str += "等"

            validity = (
                f"{info['valid_from']} 至 {info['valid_to']}"
                if info["valid_from"] and info["valid_to"]
                else "长期有效"
            )

            markdown += f"| {info['name']} | {items_str} | {conditions_str} | {validity} | {info['status']} |\n"
    else:
        markdown += "## 1. 今天可用的优惠券\n\n暂无今天可用的优惠券\n\n"

    # 未来可用的优惠券
    if categorized_coupons["future"]:
        markdown += "\n## 2. 未来可用的优惠券\n\n"
        markdown += "| 优惠券名称 | 可购买物品 | 生效日期 | 使用条件 | 备注 |\n"
        markdown += "|------------|------------|----------|----------|------|\n"

        for coupon in categorized_coupons["future"]:
            info = extract_coupon_info(coupon)

            items_str = "、".join(info["items"][:3]) if info["items"] else "多种商品"
            conditions_str = (
                "、".join(info["conditions"][:2])
                if info["conditions"]
                else "无特殊条件"
            )

            markdown += f"| {info['name']} | {items_str} | {info['valid_from']} | {conditions_str} | 即将生效 |\n"
    else:
        markdown += "\n## 2. 未来可用的优惠券\n\n暂无未来可用的优惠券\n\n"

    # 最佳组合建议
    markdown += "\n## 3. 最佳组合使用建议\n\n"

    # 分析优惠券组合
    today_coupons = categorized_coupons["today"]
    if len(today_coupons) >= 2:
        markdown += "| 组合方案 | 包含优惠券 | 预计节省 | 使用策略 | 推荐度 |\n"
        markdown += "|----------|------------|----------|----------|--------|\n"

        # 简单组合逻辑：按折扣类型分组
        drink_coupons = []
        food_coupons = []
        combo_coupons = []

        for coupon in today_coupons:
            info = extract_coupon_info(coupon)
            desc_lower = info["description"].lower()

            if any(word in desc_lower for word in ["饮料", "饮品", "可乐", "咖啡"]):
                drink_coupons.append(info)
            elif any(word in desc_lower for word in ["汉堡", "薯条", "鸡块", "套餐"]):
                food_coupons.append(info)
            else:
                combo_coupons.append(info)

        # 生成组合建议
        combinations = []

        # 饮料+食物组合
        if drink_coupons and food_coupons:
            drink = drink_coupons[0]
            food = food_coupons[0]
            combo_name = f"{drink['name'].split(' ')[0]}+{food['name'].split(' ')[0]}"
            coupons = f"{drink['name']}, {food['name']}"
            savings = "组合节省更多"
            strategy = "先使用食物券，再使用饮料券"
            rating = "★★★★★"
            combinations.append([combo_name, coupons, savings, strategy, rating])

        # 同类优惠券组合
        if len(food_coupons) >= 2:
            food1 = food_coupons[0]
            food2 = food_coupons[1]
            combo_name = "双美食组合"
            coupons = f"{food1['name']}, {food2['name']}"
            savings = "叠加优惠"
            strategy = "分两次使用或与朋友共享"
            rating = "★★★★☆"
            combinations.append([combo_name, coupons, savings, strategy, rating])

        # 通用组合
        if combo_coupons:
            for i, combo in enumerate(combo_coupons[:2], 1):
                combo_name = f"通用优惠{i}"
                coupons = combo["name"]
                savings = combo.get("discount", "具体折扣")
                strategy = "适合任意订单"
                rating = "★★★☆☆"
                combinations.append([combo_name, coupons, savings, strategy, rating])

        # 输出组合表格
        for combo in combinations:
            markdown += (
                f"| {combo[0]} | {combo[1]} | {combo[2]} | {combo[3]} | {combo[4]} |\n"
            )
    else:
        markdown += "优惠券数量不足，无法提供组合建议。建议先领取更多优惠券。\n"

    return markdown


def main():
    """主函数"""
    print("麦当劳优惠券分析工具")
    print("=" * 50)

    # 这里应该从MCP工具获取实际数据
    # 目前使用模拟数据演示
    print("⚠️ 注意: 这是演示版本，使用模拟数据")
    print("实际使用时需要从MCP工具获取真实数据")

    # 模拟数据
    mock_coupons = [
        {
            "name": "麦辣鸡腿堡买一送一",
            "description": "购买麦辣鸡腿堡，第二个免费。适用产品:麦辣鸡腿堡;使用条件:限堂食",
            "validFrom": "2025-01-19",
            "validTo": "2025-01-25",
            "status": "可用",
        },
        {
            "name": "大薯条5折券",
            "description": "大薯条5折优惠。可购买:大薯条;条件:任意订单可用",
            "validFrom": "2025-01-20",
            "validTo": "2025-01-27",
            "status": "可用",
        },
        {
            "name": "可乐免费升级",
            "description": "中可乐免费升级为大可乐。适用产品:可乐;使用条件:购买任意套餐",
            "validFrom": "2025-01-22",
            "validTo": "2025-01-29",
            "status": "可用",
        },
        {
            "name": "新年全家桶8折",
            "description": "新年全家桶8折优惠。可购买:全家桶套餐;条件:限周末使用",
            "validFrom": "2025-01-28",
            "validTo": "2025-02-05",
            "status": "待生效",
        },
    ]

    # 分类优惠券
    categorized = categorize_coupons(mock_coupons)

    # 生成Markdown
    markdown = generate_markdown_table(categorized)

    # 输出结果
    print("\n" + markdown)

    # 保存到文件
    output_file = "coupon_analysis.md"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"\n✅ 分析报告已保存到: {output_file}")
    except Exception as e:
        print(f"❌ 保存文件时出错: {e}")


if __name__ == "__main__":
    main()
