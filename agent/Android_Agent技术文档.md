# Android Agent 技术文档

## 项目概述

Android Agent 是一个基于大语言模型（LLM）和 ADB 工具链的自动化测试验收系统。该系统能够自主阅读功能文档、操控真实 Android 设备、执行功能验证，并生成结构化的验收报告。

### 核心能力

- **文档理解**：自动解析功能需求文档，提取测试点
- **设备控制**：通过 ADB 命令操控真机或模拟器
- **智能验证**：基于 LLM 推理能力进行功能验证
- **报告生成**：输出结构化的验收测试报告

## 系统架构

### 整体架构

```
┌─────────────────────────────────────────────────────┐
│                   Android Agent                      │
├─────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ 文档解析模块  │  │  LLM推理引擎  │  │ 报告生成  │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│         │                  │                │        │
│         └──────────────────┼────────────────┘        │
│                            │                         │
│                   ┌────────▼────────┐                │
│                   │   ADB工具链     │                │
│                   └────────┬────────┘                │
└────────────────────────────┼────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Android设备    │
                    └─────────────────┘
```

### 核心组件

#### 1. 文档解析模块
- 读取功能点文档（Markdown/PDF）
- 提取测试用例和验收标准
- 生成测试任务队列

#### 2. LLM 推理引擎
- 理解功能需求语义
- 生成测试步骤
- 分析测试结果
- 决策下一步操作

#### 3. ADB 工具链
- 设备连接管理
- 应用安装/卸载
- UI 交互（点击、滑动、输入）
- 截图与日志采集
- 性能数据监控

#### 4. 报告生成模块
- 测试结果汇总
- 截图证据整理
- 问题分类统计
- 生成结构化报告

## 技术实现

### ADB 命令封装

```python
class ADBController:
    def install_apk(self, apk_path: str) -> bool
    def launch_app(self, package_name: str) -> bool
    def click(self, x: int, y: int) -> bool
    def input_text(self, text: str) -> bool
    def screenshot(self, save_path: str) -> bool
    def get_current_activity(self) -> str
    def get_ui_hierarchy(self) -> dict
```

### LLM 交互流程

1. **任务理解阶段**
   - 输入：功能文档 + APK 信息
   - 输出：测试计划

2. **执行验证阶段**
   - 输入：当前界面截图 + UI 层级树
   - 推理：下一步操作
   - 输出：ADB 命令

3. **结果判断阶段**
   - 输入：操作前后对比
   - 推理：是否符合预期
   - 输出：通过/失败 + 原因

### 工作流程

```
开始
  │
  ├─ 读取功能文档
  │
  ├─ 连接 Android 设备
  │
  ├─ 安装 APK
  │
  ├─ 遍历功能点
  │   │
  │   ├─ LLM 生成测试步骤
  │   │
  │   ├─ 执行 ADB 操作
  │   │
  │   ├─ 截图 + 获取 UI 信息
  │   │
  │   ├─ LLM 判断结果
  │   │
  │   └─ 记录测试结果
  │
  ├─ 生成验收报告
  │
结束
```

## 使用示例

### 基本用法

```python
from android_agent import AndroidAgent

# 初始化 Agent
agent = AndroidAgent(
    llm_model="claude-opus-4",
    device_id="192.168.8.153"
)

# 加载功能文档
agent.load_document("功能文档.md")

# 安装并测试 APK
agent.install_apk("app-debug.apk")

# 执行自动化验收
report = agent.run_acceptance_test()

# 生成报告
report.save("验收报告.md")
```

### 测试场景示例

**场景：验证逆向知识库 APK**

1. Agent 读取功能文档，识别 4 个功能点
2. 启动应用，截图主界面
3. 依次点击 4 个按钮
4. 验证每个页面显示的内容
5. 对比文档要求，判断是否通过
6. 生成包含截图的验收报告

## 技术栈

### 开发环境
- Python 3.8+
- Android SDK Platform Tools
- ADB 工具

### 核心依赖
- LLM API（Claude/GPT-4）
- adb-shell / pure-python-adb
- Pillow（图像处理）
- lxml（UI 层级解析）

### Android 要求
- Android 5.0+ (API 21+)
- 开启 USB 调试
- 允许 ADB 安装应用

## 优势与特点

### 1. 智能化
- 无需编写测试脚本
- 自适应不同 UI 布局
- 自然语言驱动测试

### 2. 高效性
- 自动化执行，节省人力
- 并行测试多个功能点
- 快速生成验收报告

### 3. 可扩展
- 支持自定义测试策略
- 可集成 CI/CD 流程
- 支持多设备并行测试

### 4. 可追溯
- 完整的操作日志
- 每步截图证据
- 结构化报告输出

## 应用场景

1. **APK 功能验收**：自动验证新版本功能
2. **回归测试**：快速验证核心功能未受影响
3. **兼容性测试**：多设备自动化测试
4. **UI 一致性检查**：对比设计稿与实际效果

## 未来规划

- [ ] 支持 iOS 设备（通过 libimobiledevice）
- [ ] 集成性能测试（CPU、内存、流量）
- [ ] 支持视频录制
- [ ] 多语言报告生成
- [ ] Web 可视化控制台

## 项目结构

```
android-agent/
├── agent/
│   ├── __init__.py
│   ├── adb_controller.py      # ADB 命令封装
│   ├── llm_engine.py          # LLM 交互引擎
│   ├── document_parser.py     # 文档解析
│   └── report_generator.py    # 报告生成
├── testApp/                   # 测试用例 APK
├── docs/                      # 文档目录
├── reports/                   # 测试报告输出
├── requirements.txt
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 ADB

```bash
adb devices  # 确认设备连接
```

### 3. 运行测试

```bash
python main.py --apk testApp/app/build/outputs/apk/debug/app-debug.apk \
               --doc 功能文档.md \
               --device 192.168.8.153
```

## 注意事项

1. 确保 Android 设备已开启开发者选项和 USB 调试
2. 首次连接需要在设备上授权 ADB 调试
3. LLM API 需要配置有效的 API Key
4. 建议使用 Android 12+ 设备以获得最佳兼容性

---

**版本**：1.0.0
**更新日期**：2026-03-08
**作者**：Android Agent Team
