#!/usr/bin/env python3
"""
麦当劳MCP配置脚本
自动配置opencode的麦当劳MCP服务器
"""

import os
import json
import sys
import subprocess
from pathlib import Path


def get_user_home():
    """获取用户主目录"""
    return Path.home()


def get_opencode_config_dir():
    """获取opencode配置目录"""
    home = get_user_home()
    config_dir = home / ".config" / "opencode"
    return config_dir


def check_existing_config():
    """检查现有配置"""
    config_dir = get_opencode_config_dir()
    config_file = config_dir / "opencode.json"

    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            # 检查是否已配置麦当劳MCP
            mcp_config = config.get("mcp", {}).get("mcd-mcp")
            if mcp_config:
                print("✅ 已找到现有的麦当劳MCP配置")
                return True, config
        except Exception as e:
            print(f"⚠️ 读取现有配置时出错: {e}")

    return False, None


def create_config_directory():
    """创建配置目录"""
    config_dir = get_opencode_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 创建配置目录: {config_dir}")
    return config_dir


def get_mcp_token():
    """获取用户输入的MCP token"""
    print("\n🔑 请输入你的麦当劳MCP token:")
    print("提示: token格式类似 '21lqF5yc7z5Pm9Im2TKOKMYSq3FYLcK4'")
    token = input("Token: ").strip()

    if not token:
        print("❌ token不能为空")
        sys.exit(1)

    return token


def create_opencode_config(token):
    """创建opencode配置文件"""
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
    return config


def save_config(config, config_dir):
    """保存配置文件"""
    config_file = config_dir / "opencode.json"

    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置文件已保存: {config_file}")
        return True
    except Exception as e:
        print(f"❌ 保存配置文件时出错: {e}")
        return False


def test_mcp_connection():
    """测试MCP连接"""
    print("\n🔗 测试MCP连接...")
    try:
        result = subprocess.run(
            ["opencode", "mcp", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.returncode == 0:
            print("✅ MCP连接测试成功")
            print(result.stdout)
            return True
        else:
            print("❌ MCP连接测试失败")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ 未找到opencode命令，请确保opencode已安装")
        return False
    except Exception as e:
        print(f"❌ 测试连接时出错: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("麦当劳MCP配置工具")
    print("=" * 50)

    # 检查现有配置
    has_config, existing_config = check_existing_config()

    if has_config:
        print("\n📋 现有配置:")
        print(json.dumps(existing_config, indent=2, ensure_ascii=False))

        choice = input("\n是否重新配置? (y/N): ").strip().lower()
        if choice != "y":
            print("使用现有配置")
            config = existing_config
        else:
            # 重新配置
            config_dir = create_config_directory()
            token = get_mcp_token()
            config = create_opencode_config(token)
    else:
        # 新配置
        config_dir = create_config_directory()
        token = get_mcp_token()
        config = create_opencode_config(token)

    # 保存配置
    if save_config(config, config_dir):
        # 测试连接
        if test_mcp_connection():
            print("\n🎉 麦当劳MCP配置完成!")
            print("\n下一步:")
            print("1. 运行 'opencode' 启动opencode")
            print("2. 在opencode中使用 'use the mcd-mcp tool' 来使用麦当劳MCP功能")
            print("3. 或运行自动领取优惠券脚本")
        else:
            print("\n⚠️ 配置已保存但连接测试失败，请检查网络和token")
    else:
        print("\n❌ 配置失败")


if __name__ == "__main__":
    main()
