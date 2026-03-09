"""
自定义 LangChain ChatModel — 通过 httpx 直接调用 Responses API

解决 API 代理的两个限制：
1. 拦截 OpenAI SDK 的 User-Agent (403 blocked)
2. 不支持 /v1/chat/completions，仅支持 /v1/responses
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://gmn.chuangzuoli.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.3-codex")


def _msg_to_role(msg: BaseMessage) -> str:
    if isinstance(msg, SystemMessage):
        return "developer"
    if isinstance(msg, HumanMessage):
        return "user"
    return "assistant"


class ResponsesAPIChatModel(BaseChatModel):
    """兼容 LangChain 的 ChatModel，绕过 OpenAI SDK 直接调用 Responses API。"""

    model: str = MODEL_NAME
    temperature: float = 0.0
    api_key: str = API_KEY
    base_url: str = BASE_URL

    @property
    def _llm_type(self) -> str:
        return "responses-api"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        input_msgs = [
            {"role": _msg_to_role(m), "content": m.content} for m in messages
        ]
        payload: dict[str, Any] = {
            "model": self.model,
            "input": input_msgs,
            "temperature": self.temperature,
        }

        with httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(120.0),
        ) as client:
            resp = client.post("/responses", json=payload)
            resp.raise_for_status()

        text = _extract_output_text(resp.json())
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])


def _extract_output_text(data: dict) -> str:
    """从 Responses API 返回数据中提取文本。"""
    for item in data.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    return part.get("text", "")
    return ""


def get_llm(**kwargs) -> ResponsesAPIChatModel:
    """便捷工厂函数，返回配置好的 LLM 实例。"""
    return ResponsesAPIChatModel(**kwargs)
