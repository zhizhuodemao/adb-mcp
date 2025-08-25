#!/usr/bin/env python3
"""
ADB MCP Server Implementation using FastMCP

This module contains the complete implementation of the ADB MCP server
with all 19 tools for comprehensive Android device management.
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp.server.fastmcp import FastMCP
from src.utils.adb_helper import ADBHelper

# 创建FastMCP服务器实例
mcp = FastMCP("ADB MCP Server")

@mcp.tool()
def list_devices() -> str:
    """列出所有连接的 Android 设备。

    Returns:
        str: 人类可读的设备列表或错误信息。
    """
    try:
        devices = ADBHelper.list_devices()
        
        if not devices:
            return "没有找到连接的Android设备。请确保：\n1. 设备已连接\n2. 已启用USB调试\n3. 已授权此计算机"
        
        result = "连接的Android设备：\n\n"
        for i, device in enumerate(devices, 1):
            result += f"{i}. 设备ID: {device['id']}\n"
            result += f"   状态: {device['status']}\n"
            
            # 显示额外信息
            for key, value in device.items():
                if key not in ['id', 'status']:
                    result += f"   {key}: {value}\n"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"列出设备时发生错误: {str(e)}"

@mcp.tool()
def get_device_info(device_id: str = "") -> str:
    """获取指定设备的详细信息。

    Args:
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 人类可读的设备信息或错误信息。
    """
    try:
        # 如果device_id为空字符串，传递None给ADBHelper
        device_id_param = device_id if device_id else None
        info = ADBHelper.get_device_info(device_id_param)
        
        if 'error' in info:
            return f"获取设备信息失败: {info['error']}"
        
        # 格式化重要信息
        important_props = {
            'ro.product.model': '设备型号',
            'ro.product.brand': '品牌',
            'ro.product.manufacturer': '制造商',
            'ro.build.version.release': 'Android版本',
            'ro.build.version.sdk': 'SDK版本',
            'ro.product.cpu.abi': 'CPU架构',
            'ro.build.display.id': '构建ID'
        }
        
        result = f"设备信息 {'(设备: ' + device_id + ')' if device_id else ''}:\n\n"
        
        # 显示重要属性
        for prop, label in important_props.items():
            if prop in info:
                result += f"{label}: {info[prop]}\n"
        
        # 显示电池和内存信息（如果可用）
        result += "\n其他信息:\n"
        other_info_found = False
        for key, value in info.items():
            if key.startswith(('battery', 'memory', 'storage')):
                result += f"{key}: {value}\n"
                other_info_found = True
        
        if not other_info_found:
            result += "暂无其他信息\n"
        
        return result
        
    except Exception as e:
        return f"获取设备信息时发生错误: {str(e)}"

# ==================== 应用管理工具 ====================

@mcp.tool()
def install_app(apk_path: str, device_id: str = "") -> str:
    """安装 APK 应用到 Android 设备。

    Args:
        apk_path (str): APK 文件的本地路径（绝对或相对，建议绝对路径）。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 安装结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.install_app(apk_path, device_id_param)

        if success:
            return f"✅ 应用安装成功\n路径: {apk_path}\n设备: {device_id or '默认设备'}\n输出: {stdout}"
        else:
            return f"❌ 应用安装失败\n错误: {stderr}"

    except Exception as e:
        return f"安装应用时发生错误: {str(e)}"

@mcp.tool()
def uninstall_app(package_name: str, device_id: str = "") -> str:
    """卸载 Android 应用。

    Args:
        package_name (str): 应用包名（例如 `com.example.app`）。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 卸载结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.uninstall_app(package_name, device_id_param)

        if success:
            return f"✅ 应用卸载成功\n包名: {package_name}\n设备: {device_id or '默认设备'}"
        else:
            return f"❌ 应用卸载失败\n错误: {stderr}"

    except Exception as e:
        return f"卸载应用时发生错误: {str(e)}"

@mcp.tool()
def list_packages(device_id: str = "", system_apps: bool = False) -> str:
    """列出设备上已安装的应用包。

    Args:
        device_id (str): 设备 ID；留空时使用默认/首个设备。
        system_apps (bool): 是否包含系统应用；默认 False，仅显示第三方应用。

    Returns:
        str: 应用包列表或提示信息。
    """
    try:
        device_id_param = device_id if device_id else None
        packages = ADBHelper.list_packages(device_id_param, system_apps)

        if not packages:
            return "没有找到已安装的应用包"

        app_type = "所有应用" if system_apps else "第三方应用"
        result = f"设备上的{app_type} (共{len(packages)}个):\n\n"

        for i, package in enumerate(packages, 1):
            result += f"{i}. {package}\n"

        return result

    except Exception as e:
        return f"列出应用包时发生错误: {str(e)}"

# ==================== 文件传输工具 ====================

@mcp.tool()
def push_file(local_path: str, remote_path: str, device_id: str = "") -> str:
    """推送文件到 Android 设备。

    Args:
        local_path (str): 本地文件路径（建议绝对路径）。
        remote_path (str): 设备上的目标路径。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 推送结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.push_file(local_path, remote_path, device_id_param)

        if success:
            return f"✅ 文件推送成功\n本地: {local_path}\n设备: {remote_path}\n设备ID: {device_id or '默认设备'}\n详情: {stdout}"
        else:
            return f"❌ 文件推送失败\n错误: {stderr}"

    except Exception as e:
        return f"推送文件时发生错误: {str(e)}"

@mcp.tool()
def pull_file(remote_path: str, local_path: str, device_id: str = "") -> str:
    """从 Android 设备拉取文件到本地。

    Args:
        remote_path (str): 设备上的文件路径。
        local_path (str): 本地保存路径（建议绝对路径）。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 拉取结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.pull_file(remote_path, local_path, device_id_param)

        if success:
            return f"✅ 文件拉取成功\n设备: {remote_path}\n本地: {local_path}\n设备ID: {device_id or '默认设备'}\n详情: {stdout}"
        else:
            return f"❌ 文件拉取失败\n错误: {stderr}"

    except Exception as e:
        return f"拉取文件时发生错误: {str(e)}"

@mcp.tool()
def list_files(remote_path: str, device_id: str = "") -> str:
    """列出 Android 设备上指定目录的文件。

    Args:
        remote_path (str): 设备上的目录路径。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 目录内容的表格文本或提示信息。
    """
    try:
        device_id_param = device_id if device_id else None
        files = ADBHelper.list_files(remote_path, device_id_param)

        if not files:
            return f"目录为空或无法访问: {remote_path}"

        result = f"目录内容: {remote_path}\n设备: {device_id or '默认设备'}\n\n"
        result += f"{'权限':<12} {'大小':<10} {'修改时间':<15} {'文件名'}\n"
        result += "-" * 60 + "\n"

        for file_info in files:
            result += f"{file_info['permissions']:<12} {file_info['size']:<10} {file_info['date']:<15} {file_info['name']}\n"

        return result

    except Exception as e:
        return f"列出文件时发生错误: {str(e)}"

# ==================== 系统信息工具 ====================

@mcp.tool()
def get_battery_info(device_id: str = "") -> str:
    """获取设备电池信息。

    Args:
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 人类可读的电池信息或错误信息。
    """
    try:
        device_id_param = device_id if device_id else None
        info = ADBHelper.get_battery_info(device_id_param)

        if 'error' in info:
            return f"获取电池信息失败: {info['error']}"

        result = f"电池信息 {'(设备: ' + device_id + ')' if device_id else ''}:\n\n"

        # 重要的电池信息
        important_keys = [
            'AC powered', 'USB powered', 'Wireless powered',
            'status', 'health', 'present', 'level', 'scale',
            'voltage', 'temperature', 'technology'
        ]

        for key in important_keys:
            if key in info:
                result += f"{key}: {info[key]}\n"

        return result

    except Exception as e:
        return f"获取电池信息时发生错误: {str(e)}"

@mcp.tool()
def get_memory_info(device_id: str = "") -> str:
    """获取设备内存信息。

    Args:
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 人类可读的内存信息或错误信息。
    """
    try:
        device_id_param = device_id if device_id else None
        info = ADBHelper.get_memory_info(device_id_param)

        if 'error' in info:
            return f"获取内存信息失败: {info['error']}"

        result = f"内存信息 {'(设备: ' + device_id + ')' if device_id else ''}:\n\n"

        # 重要的内存信息
        important_keys = [
            'MemTotal', 'MemFree', 'MemAvailable', 'Buffers', 'Cached',
            'SwapTotal', 'SwapFree', 'Active', 'Inactive'
        ]

        for key in important_keys:
            if key in info:
                result += f"{key}: {info[key]}\n"

        return result

    except Exception as e:
        return f"获取内存信息时发生错误: {str(e)}"

@mcp.tool()
def get_storage_info(device_id: str = "") -> str:
    """获取设备存储信息。

    Args:
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 人类可读的存储信息表格或错误信息。
    """
    try:
        device_id_param = device_id if device_id else None
        storage_list = ADBHelper.get_storage_info(device_id_param)

        if not storage_list:
            return "无法获取存储信息"

        result = f"存储信息 {'(设备: ' + device_id + ')' if device_id else ''}:\n\n"
        result += f"{'文件系统':<20} {'大小':<10} {'已用':<10} {'可用':<10} {'使用率':<8} {'挂载点'}\n"
        result += "-" * 80 + "\n"

        for storage in storage_list:
            result += f"{storage['filesystem']:<20} {storage['size']:<10} {storage['used']:<10} {storage['available']:<10} {storage['use_percent']:<8} {storage['mounted_on']}\n"

        return result

    except Exception as e:
        return f"获取存储信息时发生错误: {str(e)}"

# ==================== 屏幕操作工具 ====================

@mcp.tool()
def take_screenshot(save_path: str, device_id: str = "") -> str:
    """截取设备屏幕。

    Args:
        save_path (str): 本地保存路径（必填，必须为绝对路径）。相对路径会相对 MCP 服务器进程工作目录解析，无法指向调用方项目目录。若需保存到调用方项目，请传入调用方项目的绝对路径。目标目录应由调用方预先创建。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 截图结果的文本信息。

    Notes:
        实际截图为 PNG 数据，建议使用 .png 扩展名。
    """
    try:
        if not save_path or not save_path.strip():
            return "❌ 参数错误: 需要提供保存路径 save_path"

        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.take_screenshot(save_path, device_id_param)

        if success:
            return f"✅ 截屏成功\n保存位置: {save_path}\n设备: {device_id or '默认设备'}"
        else:
            return f"❌ 截屏失败\n错误: {stderr}"

    except Exception as e:
        return f"截屏时发生错误: {str(e)}"

@mcp.tool()
def record_screen(duration: int = 10, save_path: str = "", device_id: str = "") -> str:
    """录制设备屏幕。

    Args:
        duration (int): 录制时长（秒），默认 10 秒。
        save_path (str): 本地保存路径（建议绝对路径）。为空时仅保存在设备上并返回设备路径提示。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 录屏结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.record_screen(duration, save_path, device_id_param)

        if success:
            if save_path:
                return f"✅ 录屏成功\n时长: {duration}秒\n保存位置: {save_path}\n设备: {device_id or '默认设备'}"
            else:
                return f"✅ 录屏成功\n时长: {duration}秒\n{stdout}\n设备: {device_id or '默认设备'}"
        else:
            return f"❌ 录屏失败\n错误: {stderr}"

    except Exception as e:
        return f"录屏时发生错误: {str(e)}"

# ==================== 输入模拟工具 ====================

@mcp.tool()
def send_text(text: str, device_id: str = "") -> str:
    """向设备发送文本输入。

    Args:
        text (str): 要发送的文本内容。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 输入结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.send_text(text, device_id_param)

        if success:
            return f"✅ 文本发送成功\n内容: {text}\n设备: {device_id or '默认设备'}"
        else:
            return f"❌ 文本发送失败\n错误: {stderr}"

    except Exception as e:
        return f"发送文本时发生错误: {str(e)}"

@mcp.tool()
def send_keyevent(keycode: int, device_id: str = "") -> str:
    """向设备发送按键事件。

    Args:
        keycode (int): 按键代码（如 4=返回键, 3=Home, 82=菜单）。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 操作结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.send_keyevent(keycode, device_id_param)

        # 常用按键代码说明
        key_names = {
            3: "Home键", 4: "返回键", 26: "电源键", 24: "音量+", 25: "音量-",
            82: "菜单键", 84: "搜索键", 67: "删除键", 66: "回车键"
        }
        key_name = key_names.get(keycode, f"按键{keycode}")

        if success:
            return f"✅ 按键发送成功\n按键: {key_name} (代码: {keycode})\n设备: {device_id or '默认设备'}"
        else:
            return f"❌ 按键发送失败\n错误: {stderr}"

    except Exception as e:
        return f"发送按键时发生错误: {str(e)}"

@mcp.tool()
def send_tap(x: int, y: int, device_id: str = "") -> str:
    """向设备发送点击事件。

    Args:
        x (int): 点击的 X 坐标。
        y (int): 点击的 Y 坐标。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 操作结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.send_tap(x, y, device_id_param)

        if success:
            return f"✅ 点击发送成功\n坐标: ({x}, {y})\n设备: {device_id or '默认设备'}"
        else:
            return f"❌ 点击发送失败\n错误: {stderr}"

    except Exception as e:
        return f"发送点击时发生错误: {str(e)}"

@mcp.tool()
def send_swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300, device_id: str = "") -> str:
    """向设备发送滑动事件。

    Args:
        x1 (int): 起始 X 坐标。
        y1 (int): 起始 Y 坐标。
        x2 (int): 结束 X 坐标。
        y2 (int): 结束 Y 坐标。
        duration (int): 滑动持续时间（毫秒），默认 300ms。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 操作结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.send_swipe(x1, y1, x2, y2, duration, device_id_param)

        if success:
            return f"✅ 滑动发送成功\n起点: ({x1}, {y1})\n终点: ({x2}, {y2})\n持续时间: {duration}ms\n设备: {device_id or '默认设备'}"
        else:
            return f"❌ 滑动发送失败\n错误: {stderr}"

    except Exception as e:
        return f"发送滑动时发生错误: {str(e)}"

# ==================== 日志工具 ====================

@mcp.tool()
def get_logcat(filter_tag: str = "", lines: int = 100, device_id: str = "") -> str:
    """获取设备日志（logcat）。

    Args:
        filter_tag (str): 过滤标签，仅显示包含此标签的日志；为空则不过滤。
        lines (int): 显示日志的行数，默认 100 行。
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 日志文本或提示信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.get_logcat(filter_tag, lines, device_id_param)

        if success:
            if not stdout.strip():
                return f"没有找到日志内容\n过滤标签: {filter_tag or '无'}\n设备: {device_id or '默认设备'}"

            result = f"设备日志 {'(设备: ' + device_id + ')' if device_id else ''}:\n"
            if filter_tag:
                result += f"过滤标签: {filter_tag}\n"
            result += f"显示行数: {lines}\n\n"
            result += stdout

            return result
        else:
            return f"❌ 获取日志失败\n错误: {stderr}"

    except Exception as e:
        return f"获取日志时发生错误: {str(e)}"

@mcp.tool()
def clear_logcat(device_id: str = "") -> str:
    """清除设备日志（logcat -c）。

    Args:
        device_id (str): 设备 ID；留空时使用默认/首个设备。

    Returns:
        str: 清除结果的文本信息。
    """
    try:
        device_id_param = device_id if device_id else None
        success, stdout, stderr = ADBHelper.clear_logcat(device_id_param)

        if success:
            return f"✅ 日志清除成功\n设备: {device_id or '默认设备'}"
        else:
            return f"❌ 日志清除失败\n错误: {stderr}"

    except Exception as e:
        return f"清除日志时发生错误: {str(e)}"

def main():
    """主函数"""
    print("启动ADB MCP服务器...")
    print("使用 Ctrl+C 停止服务器")
    mcp.run()

if __name__ == "__main__":
    main()
