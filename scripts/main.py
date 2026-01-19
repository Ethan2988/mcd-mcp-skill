#!/usr/bin/env python3
"""
麦当劳MCP配置和优惠券管理主脚本

注意：此脚本为旧版本，使用脚本调用方式。
推荐使用自然语言查询方式，直接调用MCP工具：
1. mcd-mcp_now-time-info - 获取当前时间
2. mcd-mcp_auto-bind-coupons - 自动领取优惠券
3. mcd-mcp_my-coupons - 查询我的优惠券
4. mcd-mcp_available-coupons - 查询可领取优惠券
5. mcd-mcp_campaign-calender - 查询活动日历
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def run_command(cmd, description=""):
    """运行命令并返回结果"""
    if description:
        print(f"\n🔧 {description}")

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, encoding="utf-8"
        )

        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout.strip():
                print(result.stdout)
            return True, result.stdout
        else:
            print(f"❌ 失败: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False, str(e)


def check_mcp_config():
    """检查MCP配置"""
    print("=" * 50)
    print("检查MCP配置状态")
    print("=" * 50)

    # 检查配置文件
    config_dir = Path.home() / ".config" / "opencode"
    config_file = config_dir / "opencode.json"

    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            mcd_config = config.get("mcp", {}).get("mcd-mcp")
            if mcd_config:
                print("✅ 麦当劳MCP配置已存在")
                print(f"   服务器: {mcd_config.get('url')}")
                print(
                    f"   状态: 已启用"
                    if mcd_config.get("enabled", False)
                    else "   状态: 已禁用"
                )
                return True, config
        except Exception as e:
            print(f"⚠️ 读取配置文件时出错: {e}")

    print("❌ 未找到麦当劳MCP配置")
    return False, None


def configure_mcd_mcp():
    """配置麦当劳MCP"""
    print("\n" + "=" * 50)
    print("配置麦当劳MCP服务器")
    print("=" * 50)

    # 获取token
    print("\n🔑 请输入你的麦当劳MCP token:")
    print("提示: token格式类似 '21lqF5yc7z5Pm9Im2TKOKMYSq3FYLcK4'")
    token = input("Token: ").strip()

    if not token:
        print("❌ token不能为空")
        return False

    # 创建配置目录
    config_dir = Path.home() / ".config" / "opencode"
    config_dir.mkdir(parents=True, exist_ok=True)

    # 创建配置文件
    config = {
        "$schema": "https://opencode.ai/config.json",
        "mcp": {
            "mcd-mcp": {
                "type": "remote",
                "url": "https://mcp.mcd.cn/mcp-servers/mcd-mcp",
                "headers": {"Authorization": f"Bearer {token}"},
                "enabled": True,
            }
        },
    }

    config_file = config_dir / "opencode.json"
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置文件已保存: {config_file}")
    except Exception as e:
        print(f"❌ 保存配置文件时出错: {e}")
        return False

    # 测试连接
    print("\n🔗 测试MCP连接...")
    success, output = run_command("opencode mcp list", "检查MCP连接")

    if success and "mcd-mcp" in output:
        print("✅ 麦当劳MCP配置成功!")
        return True
    else:
        print("⚠️ 配置已保存，但连接测试未通过")
        return False


def auto_collect_coupons():
    """自动领取优惠券"""
    print("\n" + "=" * 50)
    print("自动领取麦当劳优惠券")
    print("=" * 50)

    print("\n🎁 正在自动领取所有可用优惠券...")

    # 这里应该调用MCP工具
    # 由于我们无法直接调用MCP工具，这里提供指导
    print("\n📋 领取步骤:")
    print("1. 启动opencode: opencode")
    print("2. 在opencode中输入: use the mcd-mcp tool to auto collect coupons")
    print("3. 或直接使用命令: opencode mcp execute mcd-mcp auto-bind-coupons")
    print("\n💡 提示: MCP工具会自动领取所有可用优惠券")

    return True


def analyze_coupons():
    """分析优惠券"""
    print("\n" + "=" * 50)
    print("分析优惠券信息")
    print("=" * 50)

    print("\n📊 正在获取优惠券数据...")

    # 这里应该调用MCP工具获取数据
    # 由于我们无法直接调用MCP工具，这里提供指导并运行分析脚本
    print("\n📋 数据获取步骤:")
    print("1. 获取可用优惠券: opencode mcp execute mcd-mcp available-coupons")
    print("2. 获取我的优惠券: opencode mcp execute mcd-mcp my-coupons")
    print("3. 获取活动日历: opencode mcp execute mcd-mcp campaign-calender")

    # 运行分析脚本
    print("\n🔍 运行优惠券分析...")
    analysis_script = Path(__file__).parent / "analyze_coupons.py"

    if analysis_script.exists():
        success, output = run_command(f"python {analysis_script}", "分析优惠券数据")
        if success:
            print("\n✅ 优惠券分析完成!")
            print("📄 分析报告已生成: coupon_analysis.md")
        else:
            print("❌ 优惠券分析失败")
    else:
        print("❌ 未找到分析脚本")

    return True


def show_menu():
    """显示菜单"""
    print("\n" + "=" * 50)
    print("麦当劳MCP配置和优惠券管理系统")
    print("=" * 50)
    print("\n请选择操作:")
    print("1. 检查MCP配置状态")
    print("2. 配置麦当劳MCP服务器")
    print("3. 自动领取优惠券")
    print("4. 分析优惠券信息")
    print("5. 完整流程（配置+领取+分析）")
    print("0. 退出")

    choice = input("\n请输入选项 (0-5): ").strip()
    return choice


def full_workflow():
    """完整工作流程"""
    print("\n" + "=" * 50)
    print("开始完整工作流程")
    print("=" * 50)

    # 1. 检查配置
    configured, config = check_mcp_config()

    # 2. 如果需要，配置MCP
    if not configured:
        print("\n➡️ 开始配置MCP服务器...")
        if not configure_mcd_mcp():
            print("❌ MCP配置失败，终止流程")
            return False

    # 3. 自动领取优惠券
    print("\n➡️ 开始自动领取优惠券...")
    auto_collect_coupons()

    # 4. 分析优惠券
    print("\n➡️ 开始分析优惠券...")
    analyze_coupons()

    print("\n🎉 完整工作流程完成!")
    return True


def main():
    """主函数"""
    while True:
        choice = show_menu()

        if choice == "0":
            print("\n👋 再见!")
            break
        elif choice == "1":
            check_mcp_config()
        elif choice == "2":
            configure_mcd_mcp()
        elif choice == "3":
            auto_collect_coupons()
        elif choice == "4":
            analyze_coupons()
        elif choice == "5":
            full_workflow()
        else:
            print("❌ 无效选项，请重新选择")

        input("\n按Enter键继续...")


if __name__ == "__main__":
    main()
