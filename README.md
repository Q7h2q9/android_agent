# android_agent

基于 LLM 驱动的 Android APK 功能自动化验收测试 Agent。

输入一个 APK 和功能文档，Agent 自主操作真机，逐项验证功能点是否与预期一致，最终生成结构化验收报告。

## 技术栈

- **LLM**：OpenAI Responses API + httpx
- **Agent 框架**：LangChain（Tool 抽象）
- **设备控制**：ADB + UI Automator
- **语言**：Python 3

## 快速开始

```bash
cd agent
pip install -r requirements.txt
```

配置 `agent/.env`：

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://your-api-endpoint/v1
MODEL_NAME=your-model-name
```

配置 `agent/app_config.json`：

```json
{
  "package": "com.example.yourapp",
  "activity": "com.example.yourapp.MainActivity"
}
```

运行：

```bash
cd agent
python interactive_agent.py
```

## 项目结构

```
├── agent/
│   ├── interactive_agent.py   # CLI 入口
│   ├── android_agent.py       # Agent 核心循环
│   ├── llm.py                 # 自定义 LangChain ChatModel
│   ├── prompt.py              # 系统提示词
│   ├── app_config.json        # 目标应用配置
│   └── tools/
│       ├── android_tools.py   # LangChain @tool 封装
│       └── adb_tools.py       # ADB 底层实现
└── testApp/                   # 示例被测应用（Kotlin）
```
