import subprocess
import json
from typing import List, Dict, Optional, Tuple

class ADBHelper:
    """ADB命令封装类"""
    
    @staticmethod
    def run_adb_command(command: List[str], timeout: int = 30) -> Tuple[bool, str, str]:
        """
        执行ADB命令
        
        Args:
            command: ADB命令列表
            timeout: 超时时间（秒）
            
        Returns:
            (success, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ['adb'] + command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except FileNotFoundError:
            return False, "", "ADB not found. Please install Android SDK platform-tools"
        except Exception as e:
            return False, "", str(e)
    
    @staticmethod
    def list_devices() -> List[Dict[str, str]]:
        """列出连接的设备"""
        success, stdout, stderr = ADBHelper.run_adb_command(['devices', '-l'])
        
        if not success:
            return []
        
        devices = []
        lines = stdout.split('\n')[1:]  # 跳过第一行标题
        
        for line in lines:
            if line.strip() and not line.startswith('*'):
                parts = line.split()
                if len(parts) >= 2:
                    device_id = parts[0]
                    status = parts[1]
                    
                    # 解析设备信息
                    device_info = {
                        'id': device_id,
                        'status': status
                    }
                    
                    # 解析额外信息（如果有）
                    for part in parts[2:]:
                        if ':' in part:
                            key, value = part.split(':', 1)
                            device_info[key] = value
                    
                    devices.append(device_info)
        
        return devices
    
    @staticmethod
    def get_device_info(device_id: Optional[str] = None) -> Dict[str, str]:
        """获取设备详细信息"""
        cmd = ['shell', 'getprop']
        if device_id:
            cmd = ['-s', device_id] + cmd
            
        success, stdout, stderr = ADBHelper.run_adb_command(cmd)
        
        if not success:
            return {'error': stderr}
        
        info = {}
        for line in stdout.split('\n'):
            if line.strip() and line.startswith('[') and ']:' in line:
                try:
                    # 解析格式: [key]: [value]
                    key_end = line.find(']:')
                    key = line[1:key_end]
                    value = line[key_end + 3:].strip()
                    if value.startswith('[') and value.endswith(']'):
                        value = value[1:-1]
                    info[key] = value
                except:
                    continue
        
        return info

    # ==================== 应用管理方法 ====================

    @staticmethod
    def install_app(apk_path: str, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """安装APK应用"""
        cmd = ['install', apk_path]
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd, timeout=120)  # 安装可能需要更长时间

    @staticmethod
    def uninstall_app(package_name: str, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """卸载应用"""
        cmd = ['uninstall', package_name]
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd)

    @staticmethod
    def list_packages(device_id: Optional[str] = None, system_apps: bool = False) -> List[str]:
        """列出已安装的应用包"""
        cmd = ['shell', 'pm', 'list', 'packages']
        if not system_apps:
            cmd.append('-3')  # 只显示第三方应用

        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return []

        packages = []
        for line in stdout.split('\n'):
            if line.startswith('package:'):
                package_name = line.replace('package:', '').strip()
                packages.append(package_name)

        return packages

    # ==================== 文件传输方法 ====================

    @staticmethod
    def push_file(local_path: str, remote_path: str, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """推送文件到设备"""
        cmd = ['push', local_path, remote_path]
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd, timeout=300)  # 文件传输可能需要更长时间

    @staticmethod
    def pull_file(remote_path: str, local_path: str, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """从设备拉取文件"""
        cmd = ['pull', remote_path, local_path]
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd, timeout=300)

    @staticmethod
    def list_files(remote_path: str, device_id: Optional[str] = None) -> List[Dict[str, str]]:
        """列出设备上的文件"""
        cmd = ['shell', 'ls', '-la', remote_path]
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return []

        files = []
        lines = stdout.split('\n')

        for line in lines:
            if line.strip() and not line.startswith('total'):
                parts = line.split()
                if len(parts) >= 8:  # 至少需要8个部分
                    # Android ls -la 输出格式: permissions links owner group size date time name
                    # 例如: drwxrwx--- 2 root everybody 3452 2025-03-07 11:16 Alarms
                    try:
                        file_info = {
                            'permissions': parts[0],
                            'links': parts[1],
                            'owner': parts[2],
                            'group': parts[3],
                            'size': parts[4],
                            'date': f"{parts[5]} {parts[6]}",
                            'name': ' '.join(parts[7:])
                        }
                        files.append(file_info)
                    except IndexError:
                        # 如果解析失败，跳过这一行
                        continue

        return files

    # ==================== 系统信息方法 ====================

    @staticmethod
    def get_battery_info(device_id: Optional[str] = None) -> Dict[str, str]:
        """获取电池信息"""
        cmd = ['shell', 'dumpsys', 'battery']
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return {'error': stderr}

        battery_info = {}
        for line in stdout.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('Current Battery Service state'):
                try:
                    key, value = line.split(':', 1)
                    battery_info[key.strip()] = value.strip()
                except:
                    continue

        return battery_info

    @staticmethod
    def get_memory_info(device_id: Optional[str] = None) -> Dict[str, str]:
        """获取内存信息"""
        cmd = ['shell', 'cat', '/proc/meminfo']
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return {'error': stderr}

        memory_info = {}
        for line in stdout.split('\n'):
            if ':' in line:
                try:
                    key, value = line.split(':', 1)
                    memory_info[key.strip()] = value.strip()
                except:
                    continue

        return memory_info

    @staticmethod
    def get_storage_info(device_id: Optional[str] = None) -> List[Dict[str, str]]:
        """获取存储信息"""
        cmd = ['shell', 'df', '-h']
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return []

        storage_info = []
        lines = stdout.split('\n')[1:]  # 跳过标题行

        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    storage_info.append({
                        'filesystem': parts[0],
                        'size': parts[1],
                        'used': parts[2],
                        'available': parts[3],
                        'use_percent': parts[4],
                        'mounted_on': ' '.join(parts[5:])
                    })

        return storage_info

    # ==================== 屏幕操作方法 ====================

    @staticmethod
    def take_screenshot(save_path: str, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """截屏（必须提供本地保存路径，且必须为绝对路径）

        注意：路径解析在MCP服务器进程侧完成，无法自动定位调用方项目目录。
        如需保存到调用方项目，请在调用侧传入调用方项目的绝对路径；
        若目标目录不存在，请在调用前创建目录，否则 adb pull 可能失败。
        """
        if not save_path or not save_path.strip():
            return False, "", "save_path is required"
        remote_path = "/sdcard/screenshot.png"

        # 先在设备上截屏
        cmd = ['shell', 'screencap', '-p', remote_path]
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return False, "", stderr

        # 拉取到本地保存路径
        return ADBHelper.pull_file(remote_path, save_path, device_id)

    @staticmethod
    def record_screen(duration: int = 10, save_path: str = "", device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """录屏"""
        remote_path = "/sdcard/screenrecord.mp4"

        # 在设备上录屏
        cmd = ['shell', 'screenrecord', '--time-limit', str(duration), remote_path]
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd, timeout=duration + 30)

        if not success:
            return False, "", stderr

        # 如果指定了保存路径，则拉取到本地
        if save_path:
            return ADBHelper.pull_file(remote_path, save_path, device_id)
        else:
            return True, f"Screen recording saved to device: {remote_path}", ""

    # ==================== 输入模拟方法 ====================

    @staticmethod
    def send_text(text: str, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """发送文本输入"""
        # 转义特殊字符
        escaped_text = text.replace(' ', '%s').replace('&', '\\&')

        cmd = ['shell', 'input', 'text', escaped_text]
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd)

    @staticmethod
    def send_keyevent(keycode: int, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """发送按键事件"""
        cmd = ['shell', 'input', 'keyevent', str(keycode)]
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd)

    @staticmethod
    def send_tap(x: int, y: int, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """发送点击事件"""
        cmd = ['shell', 'input', 'tap', str(x), str(y)]
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd)

    @staticmethod
    def send_swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """发送滑动事件"""
        cmd = ['shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)]
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd)

    # ==================== 日志方法 ====================

    @staticmethod
    def get_logcat(filter_tag: str = "", lines: int = 100, device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """获取logcat日志"""
        cmd = ['logcat', '-d']  # -d 表示dump现有日志并退出

        if lines > 0:
            cmd.extend(['-t', str(lines)])

        if filter_tag:
            cmd.append(f"{filter_tag}:*")
            cmd.append("*:S")  # 静默其他标签

        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd, timeout=60)

    @staticmethod
    def clear_logcat(device_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """清除logcat日志"""
        cmd = ['logcat', '-c']
        if device_id:
            cmd = ['-s', device_id] + cmd

        return ADBHelper.run_adb_command(cmd)

    # ==================== 系统信息方法 ====================

    @staticmethod
    def get_battery_info(device_id: Optional[str] = None) -> Dict[str, str]:
        """获取电池信息"""
        cmd = ['shell', 'dumpsys', 'battery']
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return {'error': stderr}

        battery_info = {}
        for line in stdout.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('Current Battery Service state'):
                try:
                    key, value = line.split(':', 1)
                    battery_info[key.strip()] = value.strip()
                except:
                    continue

        return battery_info

    @staticmethod
    def get_memory_info(device_id: Optional[str] = None) -> Dict[str, str]:
        """获取内存信息"""
        cmd = ['shell', 'cat', '/proc/meminfo']
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return {'error': stderr}

        memory_info = {}
        for line in stdout.split('\n'):
            if ':' in line:
                try:
                    key, value = line.split(':', 1)
                    memory_info[key.strip()] = value.strip()
                except:
                    continue

        return memory_info

    @staticmethod
    def get_storage_info(device_id: Optional[str] = None) -> List[Dict[str, str]]:
        """获取存储信息"""
        cmd = ['shell', 'df', '-h']
        if device_id:
            cmd = ['-s', device_id] + cmd

        success, stdout, stderr = ADBHelper.run_adb_command(cmd)

        if not success:
            return []

        storage_info = []
        lines = stdout.split('\n')[1:]  # 跳过标题行

        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    storage_info.append({
                        'filesystem': parts[0],
                        'size': parts[1],
                        'used': parts[2],
                        'available': parts[3],
                        'use_percent': parts[4],
                        'mounted_on': ' '.join(parts[5:])
                    })

        return storage_info
