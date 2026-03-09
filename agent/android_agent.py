"""Android Agent - 带工具执行的版本"""
from llm import get_llm
from tools.android_tools import android_tools
from prompt import ANDROID_AGENT_PROMPT
import json
import re


def execute_tool(tool_name: str, tool_input: dict):
    """执行已注册的工具"""
    # 从android_tools列表中找到对应的工具
    tool_func = None
    for tool in android_tools:
        if tool.name == tool_name:
            tool_func = tool
            break

    if not tool_func:
        return f"错误：工具 {tool_name} 不存在"

    try:
        # 调用工具
        result = tool_func.invoke(tool_input)
        return result
    except Exception as e:
        return f"执行错误: {str(e)}"


def parse_json_response(text: str) -> dict:
    """从LLM响应中提取JSON"""
    try:
        return json.loads(text)
    except:
        pass

    # 提取代码块中的JSON
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            pass

    # 提取任何JSON对象
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass

    return None


def run_agent(task: str, max_steps: int = 5):
    """运行Agent执行任务"""
    llm = get_llm(temperature=0)
    history = []

    # 尝试打开配置的应用
    try:
        with open('app_config.json', 'r', encoding='utf-8') as f:
            app_config = json.load(f)
            package = app_config.get('package')
            activity = app_config.get('activity')
            if package:
                print(f"打开应用: {package}")
                from tools import adb_tools
                adb_tools.launch_app(package, activity)
                import time
                time.sleep(2)  # 等待应用启动
    except FileNotFoundError:
        pass

    print(f"\n任务: {task}\n")
    print("=" * 50)

    for step in range(max_steps):
        print(f"\n步骤 {step + 1}:")

        # 构建提示
        prompt = f"""{ANDROID_AGENT_PROMPT}

任务：{task}

历史记录：
{json.dumps(history, ensure_ascii=False, indent=2) if history else "无"}

请返回JSON格式的下一步操作。
"""

        # 调用LLM
        response = llm.invoke(prompt)
        response_text = response.content

        # 解析JSON
        parsed = parse_json_response(response_text)

        if not parsed:
            print(f"无法解析响应:\n{response_text}")
            break

        print(f"思考: {parsed.get('thought', 'N/A')}")

        # 检查是否完成
        if parsed.get("final_answer"):
            print(f"\n最终答案:\n{parsed['final_answer']}")
            return parsed["final_answer"]

        # 执行工具
        action = parsed.get("action")
        action_input = parsed.get("action_input", {})

        if action:
            print(f"执行: {action}({action_input})")
            result = execute_tool(action, action_input)

            # 对于UI层级信息，保留更多内容
            if action == "get_ui_hierarchy":
                result_str = str(result)[:3000]  # UI层级保留3000字符
            else:
                result_str = str(result)[:500]

            print(f"结果: {result_str[:200]}...")

            # 记录历史
            history.append({
                "action": action,
                "input": action_input,
                "result": result_str
            })
        else:
            print("无操作")
            break

    return "达到最大步骤数"


if __name__ == "__main__":
    result = run_agent("获取当前界面信息")
