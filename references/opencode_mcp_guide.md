# OpenCode MCP 配置指南

## 什么是MCP？

Model Context Protocol (MCP) 是一个协议，允许外部工具集成到OpenCode中。通过MCP，你可以添加各种工具和服务到OpenCode，扩展其功能。

## 麦当劳MCP配置

### 配置格式

OpenCode的MCP配置使用JSON格式，配置文件位于：
- 用户主目录: `~/.config/opencode/opencode.json` (全局配置)
- 项目目录: `./opencode.json` (项目特定配置)

### 麦当劳MCP配置示例

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

### 配置参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 服务器类型，麦当劳MCP使用 `"remote"` |
| `url` | string | 是 | MCP服务器URL |
| `headers` | object | 是 | 请求头，包含认证信息 |
| `enabled` | boolean | 否 | 是否启用，默认 `true` |
| `timeout` | number | 否 | 超时时间(ms)，默认5000 |

## 获取麦当劳MCP Token

1. 访问麦当劳MCP服务网站
2. 注册或登录账户
3. 在个人中心获取API Token
4. Token格式通常为32位字符串，如：`21lqF5yc7z5Pm9Im2TKOKMYSq3FYLcK4`

## 验证配置

配置完成后，使用以下命令验证：

```bash
# 列出所有MCP服务器
opencode mcp list

# 测试特定MCP服务器
opencode mcp debug mcd-mcp
```

成功连接后，你会看到类似输出：
```
●  ✓ mcd-mcp connected
    https://mcp.mcd.cn/mcp-servers/mcd-mcp
```

## 使用麦当劳MCP工具

配置成功后，在OpenCode中可以使用以下方式调用麦当劳MCP工具：

### 在opencode TUI中
```
use the mcd-mcp tool to check my coupons
```

### 通过命令行
```bash
# 自动领取优惠券
opencode mcp execute mcd-mcp auto-bind-coupons

# 查询我的优惠券
opencode mcp execute mcd-mcp my-coupons

# 查询可领取优惠券
opencode mcp execute mcd-mcp available-coupons

# 查询活动日历
opencode mcp execute mcd-mcp campaign-calender
```

## 麦当劳MCP工具列表

| 工具名称 | 功能 | 参数 |
|----------|------|------|
| `mcd-mcp_auto-bind-coupons` | 自动领取所有可用优惠券 | 无 |
| `mcd-mcp_my-coupons` | 查询用户已拥有的优惠券 | `page`, `pageSize` |
| `mcd-mcp_available-coupons` | 查询当前可领取的优惠券 | 无 |
| `mcd-mcp_campaign-calender` | 查询营销活动日历 | `specifiedDate` (可选) |
| `mcd-mcp_now-time-info` | 获取当前时间信息 | 无 |

## 故障排除

### 常见问题

1. **连接失败**
   - 检查网络连接
   - 验证token是否正确
   - 确认URL地址

2. **认证失败**
   - Token可能已过期
   - 检查token格式是否正确
   - 重新获取token

3. **工具不可用**
   - 检查MCP服务器状态
   - 确认配置已启用
   - 运行 `opencode mcp list` 检查连接状态

### 调试命令

```bash
# 查看详细错误信息
opencode mcp debug mcd-mcp

# 查看MCP服务器日志
opencode mcp logs mcd-mcp

# 重新加载MCP配置
opencode mcp reload
```

## 最佳实践

1. **安全性**
   - 不要将token提交到版本控制
   - 使用环境变量存储敏感信息
   - 定期更新token

2. **性能**
   - 只启用需要的MCP服务器
   - MCP工具会增加上下文长度，谨慎使用
   - 对于大量数据，使用分页查询

3. **维护**
   - 定期检查MCP服务器更新
   - 备份配置文件
   - 监控MCP连接状态

## 相关资源

- [OpenCode MCP文档](https://opencode.ai/docs/mcp-servers/)
- [Model Context Protocol官方文档](https://spec.modelcontextprotocol.io/)
- [麦当劳MCP服务](https://mcp.mcd.cn/)