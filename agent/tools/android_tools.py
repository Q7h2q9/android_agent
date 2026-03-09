"""Android工具集 - 使用@tool装饰器"""
from langchain_core.tools import tool
from . import adb_tools as android_tools_impl


@tool
def get_current_activity() -> str:
    """获取当前显示的Activity名称"""
    return android_tools_impl.get_current_activity()


@tool
def get_app_info() -> str:
    """获取当前应用的完整信息（包名、Activity等），返回JSON格式，方便后续重新打开应用"""
    import json
    return json.dumps(android_tools_impl.get_app_info(), ensure_ascii=False, indent=2)


@tool
def get_ui_hierarchy() -> str:
    """获取当前界面的UI结构，包含所有组件的位置、文字、ID等信息"""
    import json
    return json.dumps(android_tools_impl.get_ui_hierarchy(), ensure_ascii=False, indent=2)


@tool
def screenshot(output_path: str = "screen.png") -> bool:
    """截取当前屏幕并保存到指定路径"""
    return android_tools_impl.screenshot(output_path)


@tool
def tap(x: int, y: int) -> bool:
    """点击屏幕指定坐标位置"""
    return android_tools_impl.tap(x, y)


@tool
def press_back() -> bool:
    """按下系统返回键，用于返回上一级界面"""
    return android_tools_impl.press_back()


@tool
def launch_app(package: str, activity: str = None) -> bool:
    """启动指定应用。如果不指定activity则启动默认Activity"""
    return android_tools_impl.launch_app(package, activity)


@tool
def get_clickable_elements() -> str:
    """获取当前界面所有可点击元素的列表，包含文字、坐标中心点等信息，比get_ui_hierarchy更简洁"""
    import json
    return json.dumps(android_tools_impl.get_clickable_elements(), ensure_ascii=False, indent=2)


@tool
def write_file(file_path: str, content: str) -> bool:
    """写入文件内容（覆盖模式），用于创建测试报告等"""
    return android_tools_impl.write_file(file_path, content)


@tool
def append_file(file_path: str, content: str) -> bool:
    """追加内容到文件，用于逐步记录测试结果"""
    return android_tools_impl.append_file(file_path, content)


@tool
def read_file(file_path: str) -> str:
    """读取文件内容，用于读取功能文档等"""
    return android_tools_impl.read_file(file_path)


# 导出所有工具
android_tools = [
    get_current_activity,
    get_app_info,
    get_ui_hierarchy,
    get_clickable_elements,
    screenshot,
    tap,
    press_back,
    launch_app,
    write_file,
    append_file,
    read_file
]
