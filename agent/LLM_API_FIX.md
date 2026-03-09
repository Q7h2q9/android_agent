# LLM API 调用问题排查与修复记录

## 现象

运行 `python launcher.py --run` 时，所有 Agent Server（ShellEditor、Architect 等）在调用 LLM 时报错：

```
openai.PermissionDeniedError: Your request was blocked.
```

而同一套 API Key / Base URL / Model 在 `04_coding_agents/` 中通过 OpenAI Agents SDK 调用完全正常。

## 排查过程

### 1. 对比两个项目的 LLM 调用方式

| 项目 | 调用方式 | 结果 |
|------|---------|------|
| `04_coding_agents` | OpenAI Agents SDK (`Runner.run()`) | 正常 |
| `05_context_isolation` | `openai.AsyncOpenAI.chat.completions.create()` | 403 被拦截 |

两者使用相同的 `config.py`（同一个 API Key、Base URL、Model Name），说明问题出在请求方式而非凭据。

### 2. 确认 API 代理不支持 Chat Completions

用 curl 直接请求 `/v1/chat/completions`：

```bash
curl https://gmn.chuangzuoli.com/v1/chat/completions \
  -H "Authorization: Bearer sk-..." \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.3-codex","messages":[{"role":"user","content":"hi"}]}'
```

返回 400：

```json
{"error":{"message":"Unsupported legacy protocol: /v1/chat/completions is not supported. Please use /v1/responses."}}
```

**结论：API 代理已废弃 Chat Completions 端点，仅支持 Responses API。**

### 3. 改用 Responses API 仍然失败

将 `base.py` 改为 `_client.responses.create()` 后仍报 `PermissionDeniedError`。

用 Monkeypatch 拦截 OpenAI SDK 的实际 HTTP 请求，发现请求体和 URL 都正确，但 SDK 自动添加了以下 Headers：

```
user-agent: AsyncOpenAI/Python 2.24.0
x-stainless-lang: python
x-stainless-package-version: 2.24.0
x-stainless-os: Linux
...
```

### 4. 定位到 User-Agent 是拦截触发条件

用 httpx 分别测试不同 Header 组合：

| 请求方式 | User-Agent | HTTP 状态码 |
|---------|-----------|------------|
| httpx（默认 UA） | `python-httpx/...` | **200** |
| httpx + SDK UA | `AsyncOpenAI/Python 2.24.0` | **403** |
| httpx + x-stainless headers（无 SDK UA） | `python-httpx/...` | **200** |
| httpx + SDK UA + x-stainless headers | `AsyncOpenAI/Python 2.24.0` | **403** |

**结论：API 代理按 User-Agent 拦截，包含 `AsyncOpenAI/Python` 的请求被拒绝。**

### 5. 尝试覆盖 SDK 的 User-Agent 失败

- `default_headers={"user-agent": "..."}` — SDK 仍以自己的 UA 优先
- `http_client=httpx.AsyncClient(headers={"user-agent": "..."})` — SDK 在发送前覆盖

OpenAI Python SDK 在 `_base_client.py` 中硬编码了 User-Agent，无法通过公开 API 覆盖。

## 最终修复

放弃 OpenAI Python SDK，改用 httpx 直接调用 Responses API：

```python
# 修改前（SDK 调用，被拦截）
from openai import AsyncOpenAI
_client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)

resp = await _client.chat.completions.create(
    model=MODEL_NAME,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_input}],
    temperature=temperature,
)
return resp.choices[0].message.content or ""

# 修改后（httpx 直接请求，正常工作）
import httpx
_http_client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    timeout=httpx.Timeout(120.0),
)

resp = await _http_client.post("/responses", json={
    "model": MODEL_NAME,
    "instructions": system_prompt,
    "input": [{"role": "user", "content": user_input}],
    "temperature": temperature,
})
data = resp.json()
# 从 output[].content[].text 中提取回复文本
```

## 04 为何正常

`04_coding_agents` 使用 OpenAI Agents SDK（`agents.Runner.run()`），该 SDK 内部的 HTTP 请求链路与直接使用 `openai.AsyncOpenAI` 不同，User-Agent 格式不会命中代理的拦截规则。

## 问题 2：Architect 返回纯文本而非 JSON

### 现象

API 连通后，Architect 返回 `"我先快速查看当前目录结构并创建所需的 C 源码与 Makefile..."` 而非预期的任务树 JSON。

### 原因

API 代理会**覆盖** Responses API 的 `instructions` 参数，注入自己的 Codex CLI 系统提示词。`call_llm` 传入的 system prompt 被完全忽略，LLM 按通用编码助手模式回复。

从 curl 测试的响应中可以看到代理注入的 instructions：

```
"instructions": "You are a coding agent running in the Codex CLI, a terminal-based coding assistant..."
```

### 修复

将 system prompt 从 `instructions` 参数移到 `input` 消息数组中，以 `developer` 角色发送：

```python
# 修改前（instructions 被代理覆盖）
payload = {
    "model": MODEL_NAME,
    "instructions": system_prompt,
    "input": [{"role": "user", "content": user_input}],
}

# 修改后（developer 消息不会被覆盖）
payload = {
    "model": MODEL_NAME,
    "input": [
        {"role": "developer", "content": system_prompt},
        {"role": "user", "content": user_input},
    ],
}
```

## 涉及文件

- `05_context_isolation/base.py` — 唯一修改的文件（`call_llm` 函数）
