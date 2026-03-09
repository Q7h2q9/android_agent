# testApp 功能测试报告

## 1. 应用信息
- **应用名称**：逆向知识库
- **包名**：com.example.reverseeng
- **当前Activity**：com.example.reverseeng.KnowledgeActivity4
- **完整Activity**：com.example.reverseeng/com.example.reverseeng.KnowledgeActivity4

## 2. 测试功能列表
根据技术文档与首页按钮，测试了以下4个核心功能：
1. 静态分析
2. 动态调试
3. 代码注入
4. 壳与保护

## 3. 测试过程与截图
- **首页**
  - 截图：`screenshots/home.png`

- **功能1：静态分析**
  - 操作：点击首页“静态分析”按钮进入详情页
  - 截图：`screenshots/static_analysis.png`

- **功能2：动态调试**
  - 操作：返回首页后点击“动态调试”按钮进入详情页
  - 截图：`screenshots/dynamic_debug.png`

- **功能3：代码注入**
  - 操作：返回首页后点击“代码注入”按钮进入详情页
  - 截图：`screenshots/code_injection.png`

- **功能4：壳与保护**
  - 操作：返回首页后点击第4个功能按钮进入详情页
  - 截图：`screenshots/shell_protection.png`

## 4. 测试结论
- 应用可正常启动，首页4个功能入口均可点击并成功进入对应知识页面。
- 页面跳转与返回流程正常（通过系统返回键可回到上一级）。
- 各功能页面均已完成截图留档。
- 本次功能性验证结果：**通过**。
