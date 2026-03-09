# testApp (逆向知识库) 技术文档

## 应用概述

**应用名称**：逆向知识库
**包名**：com.example.reverseeng
**版本**：1.0 (versionCode: 1)
**类型**：教育类应用

逆向知识库是一款面向逆向工程学习者的知识展示应用，提供4个核心逆向技术板块的基础知识介绍。

## 技术规格

### 开发环境
- **开发语言**：Kotlin
- **最低SDK版本**：API 31 (Android 12)
- **目标SDK版本**：API 34 (Android 14)
- **编译SDK版本**：API 36

### 构建工具
- **Gradle版本**：8.11.1
- **Android Gradle Plugin**：8.10.1
- **Kotlin版本**：2.0.21

### 依赖库
```kotlin
androidx.core:core-ktx:1.17.0
androidx.appcompat:appcompat:1.6.1
com.google.android.material:material:1.10.0
```

### Java配置
- **源码兼容性**：Java 11
- **目标兼容性**：Java 11
- **Kotlin JVM目标**：11

## 应用架构

### 项目结构
```
testApp/
├── app/
│   ├── src/main/
│   │   ├── java/com/example/reverseeng/
│   │   │   ├── MainActivity.kt
│   │   │   ├── KnowledgeActivity1.kt
│   │   │   ├── KnowledgeActivity2.kt
│   │   │   ├── KnowledgeActivity3.kt
│   │   │   └── KnowledgeActivity4.kt
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   ├── activity_main.xml
│   │   │   │   ├── activity_knowledge1.xml
│   │   │   │   ├── activity_knowledge2.xml
│   │   │   │   ├── activity_knowledge3.xml
│   │   │   │   └── activity_knowledge4.xml
│   │   │   └── values/
│   │   │       └── themes.xml
│   │   └── AndroidManifest.xml
│   └── build.gradle.kts
├── gradle/
└── build.gradle.kts
```

### 架构模式
- **UI架构**：传统Activity架构
- **导航方式**：Intent显式跳转
- **布局方式**：LinearLayout线性布局

## 功能模块

### 1. 主界面 (MainActivity)

**功能描述**：应用入口，展示4个知识板块入口

**UI组件**：
- 标题：逆向知识库
- 4个导航按钮：
  - 静态分析（蓝色 #3498DB）
  - 动态调试（红色 #E74C3C）
  - 代码注入（绿色 #2ECC71）
  - 脱壳技术（紫色 #9B59B6）

**交互逻辑**：
```kotlin
点击按钮 → startActivity() → 跳转到对应知识页面
```

### 2. 静态分析模块 (KnowledgeActivity1)

**知识内容**：
- 定义：在不运行程序的情况下分析代码结构
- 常用工具：IDA Pro、Ghidra、Jadx
- 分析内容：反编译代码、控制流图、函数调用关系

**UI特点**：
- 背景色：#3498DB（蓝色）
- 全屏沉浸式展示
- 白色文字，居中对齐

### 3. 动态调试模块 (KnowledgeActivity2)

**知识内容**：
- 定义：在程序运行时进行分析和调试
- 常用工具：GDB、LLDB、Frida
- 技术要点：断点设置、内存查看、寄存器修改

**UI特点**：
- 背景色：#E74C3C（红色）
- 全屏沉浸式展示

### 4. 代码注入模块 (KnowledgeActivity3)

**知识内容**：
- 定义：将自定义代码插入目标进程
- 常用工具：Frida、Xposed、Cydia Substrate
- 应用场景：Hook函数、修改行为、绕过检测

**UI特点**：
- 背景色：#2ECC71（绿色）
- 全屏沉浸式展示

### 5. 脱壳技术模块 (KnowledgeActivity4)

**知识内容**：
- 定义：去除程序保护层以分析原始代码
- 常见壳：UPX、VMProtect、Themida
- 脱壳方法：内存dump、OEP定位、IAT修复

**UI特点**：
- 背景色：#9B59B6（紫色）
- 全屏沉浸式展示

## UI设计

### 主题配置
```xml
Theme.ReverseEng (继承 Material Design)
- colorPrimary: #2C3E50
- colorPrimaryVariant: #1A252F
- colorOnPrimary: #FFFFFF
```

### 布局特点
- 采用LinearLayout垂直布局
- 居中对齐（gravity="center"）
- 统一内边距：32dp
- 按钮间距：16dp
- 文字大小：标题32sp，按钮18sp，内容18-20sp

### 配色方案
- 主界面背景：#F5F5F5（浅灰）
- 静态分析：#3498DB（蓝色系）
- 动态调试：#E74C3C（红色系）
- 代码注入：#2ECC71（绿色系）
- 脱壳技术：#9B59B6（紫色系）

## 技术实现细节

### Activity生命周期
```kotlin
onCreate() {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.xxx)
    // 设置点击监听器
}
```

### 页面跳转
```kotlin
findViewById<Button>(R.id.btnX).setOnClickListener {
    startActivity(Intent(this, KnowledgeActivityX::class.java))
}
```

### 资源引用
- 布局文件：R.layout.activity_xxx
- 控件ID：R.id.btnX
- 主题：R.style.Theme_ReverseEng

## APK信息

### 构建配置
- **构建类型**：Debug
- **签名方式**：Android Debug Keystore
- **混淆**：未启用（isMinifyEnabled = false）

### APK输出
- **文件路径**：`app/build/outputs/apk/debug/app-debug.apk`
- **文件大小**：约13MB
- **支持架构**：通用（未指定特定架构）

### 权限声明
无特殊权限要求（仅基础应用权限）

## 构建说明

### 构建命令
```bash
# Debug版本
./gradlew assembleDebug

# Release版本
./gradlew assembleRelease

# 清理构建
./gradlew clean
```

### 安装命令
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

### 卸载命令
```bash
adb uninstall com.example.reverseeng
```

## 兼容性

### 设备要求
- Android 12 (API 31) 及以上
- 屏幕尺寸：适配所有常见尺寸
- 屏幕方向：竖屏

### 测试设备
- 推荐：Android 12-14 设备
- 分辨率：1080x1920 及以上

## 已知限制

1. **最低版本限制**：仅支持Android 12+，不兼容旧版本系统
2. **内容静态**：知识内容硬编码在布局文件中，无动态更新
3. **无数据持久化**：不保存用户浏览记录
4. **单语言**：仅支持中文
5. **无网络功能**：纯离线应用

## 扩展建议

### 功能增强
- [ ] 添加搜索功能
- [ ] 支持内容收藏
- [ ] 添加更多知识条目
- [ ] 支持多语言
- [ ] 添加夜间模式

### 技术优化
- [ ] 使用ViewModel管理数据
- [ ] 采用Navigation组件
- [ ] 实现内容动态加载
- [ ] 添加单元测试
- [ ] 优化APK体积

## 维护信息

**版本历史**：
- v1.0 (2026-03-08)：初始版本，包含4个基础知识模块

**开发团队**：Android Agent Team
**最后更新**：2026-03-08
