# 麦当劳优惠券助手 (McDonald's Coupon Assistant)

一个帮助用户配置麦当劳MCP服务器并自动化管理优惠券的skill技能,适合opencode 使用，能够自动化配置麦当劳mcp，减少繁琐的配置mcp过程，自动领取优惠券，然后自动化安排好优惠券最佳组合使用
## 功能特性

### 🚀 核心功能
- **一键配置** - 指导用户配置麦当劳MCP服务器
- **自动领券** - 自动领取所有可用麦当劳优惠券
- **优惠券管理** - 查询可用优惠券、已拥有优惠券、活动日历
- **智能分析** - 生成优惠券使用指南和最佳组合建议
- **活动提醒** - 查看麦当劳营销活动日历

### 🔧 集成工具
- `mcd-mcp_now-time-info` - 获取当前时间信息
- `mcd-mcp_auto-bind-coupons` - 自动领取所有可用优惠券
- `mcd-mcp_my-coupons` - 查询用户已拥有的优惠券
- `mcd-mcp_available-coupons` - 查询当前可领取的优惠券列表
- `mcd-mcp_campaign-calender` - 查询麦当劳营销活动日历

## 快速开始

### 前提条件
1. **麦当劳MCP Token** - 访问 [麦当劳MCP官方文档](https://open.mcd.cn/mcp/doc) 获取
2. **OpenCode环境** - 已安装并配置OpenCode

### 使用方法

#### 方式1: 自然语言查询（推荐）
在OpenCode中直接使用自然语言调用工具：
```bash
# 获取当前时间
获取当前时间

# 自动领取优惠券
自动领取麦当劳优惠券

# 查看我的优惠券
查看我的优惠券

# 查询可领取优惠券
有哪些优惠券可以领取

# 查看活动日历
查看麦当劳活动日历
```

#### 方式2: 脚本调用
```bash
# 运行主脚本
python scripts/main.py

# 配置MCP服务器
python scripts/configure_mcd_mcp.py

# 分析优惠券数据
python scripts/analyze_coupons.py
```

## 配置指南

### 获取MCP Token
1. 访问 [麦当劳MCP官方文档](https://open.mcd.cn/mcp/doc)
2. 注册或登录账户
3. 获取个人MCP token（格式如：`21lqF5yc7z5Pm9Im2TKOKMYSq3FYLcK4`）

### 配置OpenCode
配置文件位置：`~/.config/opencode/opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "mcd-mcp": {
      "type": "remote",
      "url": "https://mcp.mcd.cn/mcp-servers/mcd-mcp",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      },
      "enabled": true
    }
  }
}
```

### 验证配置
```bash
# 检查MCP连接
opencode mcp list

# 测试麦当劳MCP
opencode mcp debug mcd-mcp
```

## 使用场景

### 🎯 场景1: 首次使用
1. 获取麦当劳MCP token
2. 配置OpenCode MCP服务器
3. 自动领取所有可用优惠券
4. 查看优惠券分析报告

### 📅 场景2: 日常查询
1. 查询今日可用优惠券
2. 查看即将到期的优惠券
3. 获取最佳组合使用建议
4. 检查新活动信息

### 🎁 场景3: 活动参与
1. 查询麦当劳营销活动日历
2. 获取活动参与指南
3. 领取活动专属优惠券
4. 跟踪活动进度

## 输出示例

### 优惠券分析报告
```markdown
## 麦当劳优惠券使用指南

### 1. 今天可用的优惠券
| 优惠券名称 | 可购买物品 | 使用条件 | 有效期 | 状态 |
|------------|------------|----------|--------|------|
| 麦辣鸡腿堡买一送一 | 麦辣鸡腿堡 | 堂食或外带 | 2025-01-20 | 可用 |
| 薯条免费升级大份 | 薯条 | 消费满30元 | 2025-01-25 | 可用 |

### 2. 最佳组合使用建议
| 组合方案 | 包含优惠券 | 预计节省 | 使用策略 | 推荐度 |
|----------|------------|----------|----------|--------|
| 午餐套餐 | 麦辣鸡腿堡买一送一 + 薯条升级 | 25元 | 两人共享 | ⭐⭐⭐⭐⭐ |

### 3. 今日到期提醒
1. **麦旋风买一送一** - 今日23:59到期，建议尽快使用
```

## 文件结构

```
mcd-mcp-skill/
├── SKILL.md              # 技能定义文件（YAML + Markdown）
├── README.md             # 项目说明文档
├── scripts/              # Python脚本
│   ├── main.py           # 主脚本（配置+领券+分析）
│   ├── configure_mcd_mcp.py  # MCP配置脚本
│   └── analyze_coupons.py    # 优惠券分析脚本
├── references/           # 参考文档
│   └── opencode_mcp_guide.md # OpenCode MCP配置指南
└── 如何获取麦当劳MCP_TOKEN.md # Token获取指南
```

## 常见问题

### ❓ 如何获取麦当劳MCP token？
访问 [麦当劳MCP官方文档](https://open.mcd.cn/mcp/doc) 注册并获取token。

### ❓ 配置后连接失败怎么办？
1. 检查网络连接
2. 验证token是否正确
3. 确认配置文件格式
4. 运行 `opencode mcp debug mcd-mcp` 查看详细错误

### ❓ 优惠券领取失败？
1. 检查账户状态
2. 确认活动时间
3. 可能没有可领取的优惠券
4. 联系麦当劳客服

### ❓ 如何更新token？
1. 获取新token
2. 更新 `~/.config/opencode/opencode.json` 文件
3. 重启OpenCode或运行 `opencode mcp reload`

## 安全提示

⚠️ **重要安全注意事项**：
1. **保护token** - 不要分享或泄露MCP token
2. **配置文件安全** - 不要提交包含token的配置文件到版本控制
3. **定期更新** - 建议定期更换token
4. **监控使用** - 关注API调用频率和异常活动

## 技术支持

- **麦当劳MCP官方文档**: https://open.mcd.cn/mcp/doc
- **OpenCode文档**: https://opencode.ai/docs/
- **问题反馈**: 在GitHub仓库提交issue

## 许可证

本项目遵循MIT许可证。

---

**提示**: 本技能为第三方开发工具，与麦当劳官方无直接关联。使用前请阅读麦当劳MCP服务条款。
