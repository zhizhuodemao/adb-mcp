# ADB MCP Tools Reference

Complete reference for all 19 tools provided by the ADB MCP server.

## 📱 设备管理 (2个工具)

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| `list_devices` | 列出所有连接的Android设备 | 无 |
| `get_device_info` | 获取设备详细信息 | device_id (可选) |

## 📦 应用管理 (3个工具)

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| `install_app` | 安装APK应用到设备 | apk_path, device_id (可选) |
| `uninstall_app` | 卸载设备上的应用 | package_name, device_id (可选) |
| `list_packages` | 列出已安装的应用包 | device_id (可选), system_apps |

## 📁 文件传输 (3个工具)

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| `push_file` | 推送文件到设备 | local_path, remote_path, device_id (可选) |
| `pull_file` | 从设备拉取文件 | remote_path, local_path, device_id (可选) |
| `list_files` | 列出设备上的文件和目录 | remote_path, device_id (可选) |

## 🔋 系统信息 (3个工具)

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| `get_battery_info` | 获取电池状态信息 | device_id (可选) |
| `get_memory_info` | 获取内存使用情况 | device_id (可选) |
| `get_storage_info` | 获取存储空间信息 | device_id (可选) |

## 📺 屏幕操作 (2个工具)

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| `take_screenshot` | 截取设备屏幕 | save_path (必填), device_id (可选) |
| `record_screen` | 录制设备屏幕 | duration, save_path (可选), device_id (可选) |

## ⌨️ 输入模拟 (4个工具)

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| `send_text` | 发送文本输入 | text, device_id (可选) |
| `send_keyevent` | 发送按键事件 | keycode, device_id (可选) |
| `send_tap` | 发送点击事件 | x, y, device_id (可选) |
| `send_swipe` | 发送滑动事件 | x1, y1, x2, y2, duration, device_id (可选) |

## 📝 日志调试 (2个工具)

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| `get_logcat` | 获取设备日志 | filter_tag (可选), lines, device_id (可选) |
| `clear_logcat` | 清除设备日志 | device_id (可选) |

## 🎯 工具分类使用建议

### 🔰 基础工具 (必备)
- `list_devices` - 检查设备连接
- `get_device_info` - 获取设备基本信息
- `list_packages` - 查看已安装应用

### 🛠️ 开发工具 (开发必备)
- `install_app` / `uninstall_app` - 应用部署
- `push_file` / `pull_file` - 文件传输
- `get_logcat` - 日志调试

### 📊 监控工具 (运维推荐)
- `get_battery_info` - 电池监控
- `get_memory_info` - 内存监控
- `get_storage_info` - 存储监控

### 🎮 自动化工具 (测试推荐)
- `take_screenshot` - 截图验证
- `send_tap` / `send_swipe` - 操作模拟
- `send_text` - 数据输入
- `record_screen` - 过程录制

### 🔧 高级工具 (专业用户)
- `send_keyevent` - 系统级操作
- `list_files` - 文件系统浏览
- `clear_logcat` - 日志管理

## 📋 快速参考

### 常用按键代码
```
3  = Home键        4  = 返回键       26 = 电源键
24 = 音量+         25 = 音量-       82 = 菜单键
67 = 删除键        66 = 回车键       84 = 搜索键
```

### 常用设备路径
```
/sdcard/                    # 外部存储根目录
/sdcard/Download/           # 下载目录
/sdcard/Pictures/           # 图片目录
/sdcard/DCIM/Camera/        # 相机照片
/data/local/tmp/            # 临时目录（需要权限）
```

### 文件格式支持
```
APK安装: .apk
截图格式: .png
录屏格式: .mp4
文件传输: 所有格式
```

## 🚀 性能提示

1. **批量操作**: 对于多个文件或应用，建议逐个操作而非并发
2. **超时设置**: 大文件传输和应用安装会自动使用更长的超时时间
3. **设备选择**: 多设备环境下建议明确指定device_id
4. **权限要求**: 某些操作需要设备已授权USB调试
5. **存储空间**: 文件传输前建议检查设备存储空间

## 🔍 故障排除

- **设备未找到**: 检查USB连接和调试授权
- **权限拒绝**: 确保设备已授权此计算机
- **文件不存在**: 检查路径是否正确
- **应用安装失败**: 检查APK兼容性和存储空间
- **输入无响应**: 确保设备屏幕已解锁

---

**总计: 19个工具，覆盖Android设备管理的所有核心需求**
