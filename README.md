# ADB MCP Server

A comprehensive Model Context Protocol (MCP) server for Android Debug Bridge (ADB) operations, providing complete Android device management capabilities.

## 功能特性

- **设备管理**: 列出设备、获取设备信息
- **应用管理**: 安装、卸载、列出应用包
- **文件传输**: 推送、拉取、列出文件
- **系统信息**: 电池、内存、存储状态
- **屏幕操作**: 截屏、录屏
- **输入模拟**: 文本输入、按键、点击、滑动
- **日志调试**: 获取、清除设备日志
- **多设备支持**: 同时管理多个Android设备
- **完整错误处理**: 详细的错误信息和故障排除

## Prerequisites

1. **Android SDK Platform Tools**: Ensure `adb` command is available in your PATH
2. **Python 3.10+**: Required for MCP server
3. **Android Device**: Connected via USB with USB debugging enabled

## Installation

```bash
# Clone the repository
git clone https://github.com/zhizhuodemao/adb-mcp
cd adb-mcp

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Start the MCP Server
```bash
python server.py
```

### Using with MCP Inspector (Development)
```bash
mcp dev server.py
```

### 可用工具

#### 设备管理
1. **list_devices** - 列出所有连接的Android设备
2. **get_device_info** - 获取设备详细信息

#### 应用管理
3. **install_app** - 安装APK应用到设备
4. **uninstall_app** - 卸载设备上的应用
5. **list_packages** - 列出已安装的应用包

#### 文件传输
6. **push_file** - 推送文件到设备
7. **pull_file** - 从设备拉取文件
8. **list_files** - 列出设备上的文件和目录

#### 系统信息
9. **get_battery_info** - 获取电池状态信息
10. **get_memory_info** - 获取内存使用情况
11. **get_storage_info** - 获取存储空间信息

#### 屏幕操作
12. **take_screenshot** - 截取设备屏幕（需要提供save_path）
13. **record_screen** - 录制设备屏幕

#### 输入模拟
14. **send_text** - 发送文本输入
15. **send_keyevent** - 发送按键事件
16. **send_tap** - 发送点击事件
17. **send_swipe** - 发送滑动事件

#### 日志调试
18. **get_logcat** - 获取设备日志
19. **clear_logcat** - 清除设备日志

## 开发调试

### 测试ADB连接
```bash
adb devices
```

### 查看日志
服务器会输出详细的调试日志，包括工具调用和错误信息。

### 使用MCP Inspector测试
```bash
# 安装后使用MCP Inspector测试
uv run mcp dev run_server.py
```

## 扩展开发

要添加新的ADB工具：

1. 在 `src/tools/` 目录下创建新的工具模块
2. 在工具类中实现 `get_tools()` 和 `handle_tool_call()` 方法
3. 在 `src/server.py` 中注册新的工具处理器

## 故障排除

1. **ADB not found**: 确保Android SDK platform-tools已安装并在PATH中
2. **No devices found**: 检查设备连接和USB调试设置
3. **Permission denied**: 确保已在设备上授权此计算机

## 项目结构

```
adb-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py          # MCP服务器主文件
│   ├── tools/
│   │   ├── __init__.py
│   │   └── device_tools.py # ADB工具实现
│   └── utils/
│       ├── __init__.py
│       └── adb_helper.py   # ADB命令封装
├── requirements.txt
├── README.md
└── run_server.py          # 启动脚本
```
