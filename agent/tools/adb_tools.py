"""Android ADB 工具集 - 5个核心功能"""
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def tap(x: int, y: int) -> bool:
    """点击屏幕指定位置"""
    result = subprocess.run(
        f"adb shell input tap {x} {y}",
        shell=True,
        capture_output=True
    )
    return result.returncode == 0


def press_back() -> bool:
    """按下系统返回键"""
    result = subprocess.run(
        "adb shell input keyevent KEYCODE_BACK",
        shell=True,
        capture_output=True
    )
    return result.returncode == 0


def get_ui_hierarchy() -> dict:
    """获取UI层次结构"""
    # Dump UI to device
    subprocess.run("adb shell uiautomator dump /sdcard/ui.xml", shell=True)
    # Pull to local
    subprocess.run("adb pull /sdcard/ui.xml ui.xml", shell=True)

    # Parse XML
    tree = ET.parse("ui.xml")
    root = tree.getroot()

    return _parse_node(root)


def _parse_node(node) -> dict:
    """解析UI节点"""
    result = {
        "class": node.get("class", ""),
        "text": node.get("text", ""),
        "resource-id": node.get("resource-id", ""),
        "bounds": node.get("bounds", ""),
        "clickable": node.get("clickable", "false"),
        "children": []
    }

    for child in node:
        result["children"].append(_parse_node(child))

    return result


def screenshot(output_path: str = "screen.png") -> bool:
    """截取屏幕"""
    result = subprocess.run(
        f"adb exec-out screencap -p > {output_path}",
        shell=True
    )
    return result.returncode == 0 and Path(output_path).exists()


def launch_app(package: str, activity: str = None) -> bool:
    """启动应用"""
    if activity:
        cmd = f"adb shell am start -n {package}/{activity}"
    else:
        cmd = f"adb shell monkey -p {package} -c android.intent.category.LAUNCHER 1"

    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.returncode == 0


def get_current_activity() -> str:
    """获取当前Activity"""
    result = subprocess.run(
        "adb shell dumpsys window | grep mCurrentFocus",
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        # 输出格式: mCurrentFocus=Window{xxx u0 package/activity}
        output = result.stdout.strip()
        if "/" in output:
            return output.split("/")[-1].rstrip("}")

    return ""


def get_clickable_elements() -> list:
    """获取所有可点击元素的简洁列表"""
    subprocess.run("adb shell uiautomator dump /sdcard/ui.xml", shell=True)
    subprocess.run("adb pull /sdcard/ui.xml ui.xml", shell=True)

    tree = ET.parse("ui.xml")
    root = tree.getroot()

    clickable_elements = []
    _extract_clickable(root, clickable_elements)
    return clickable_elements


def _extract_clickable(node, result: list):
    """递归提取可点击元素"""
    if node.get("clickable") == "true":
        bounds = node.get("bounds", "")
        # 解析bounds计算中心点
        if bounds:
            # bounds格式: [x1,y1][x2,y2]
            import re
            match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
            if match:
                x1, y1, x2, y2 = map(int, match.groups())
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                result.append({
                    "text": node.get("text", ""),
                    "resource-id": node.get("resource-id", ""),
                    "class": node.get("class", ""),
                    "bounds": bounds,
                    "center": [center_x, center_y]
                })

    for child in node:
        _extract_clickable(child, result)


def get_app_info() -> dict:
    """获取当前应用的完整信息（包名、Activity等）"""
    result = subprocess.run(
        "adb shell dumpsys window | grep mCurrentFocus",
        shell=True,
        capture_output=True,
        text=True
    )

    info = {
        "package": "",
        "activity": "",
        "full_activity": ""
    }

    if result.returncode == 0:
        # 输出格式: mCurrentFocus=Window{xxx u0 package/activity}
        output = result.stdout.strip()
        if "/" in output:
            # 提取 package/activity 部分
            parts = output.split()
            for part in parts:
                if "/" in part:
                    full = part.rstrip("}")
                    package, activity = full.split("/", 1)
                    info["package"] = package
                    info["activity"] = activity
                    info["full_activity"] = full
                    break

    return info


def write_file(file_path: str, content: str) -> bool:
    """写入文件内容（覆盖模式）"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"写入文件失败: {e}")
        return False


def append_file(file_path: str, content: str) -> bool:
    """追加内容到文件"""
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"追加文件失败: {e}")
        return False


def read_file(file_path: str) -> str:
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件失败: {e}"
