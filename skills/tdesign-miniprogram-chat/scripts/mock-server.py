#!/usr/bin/env python3
"""
TDesign Miniprogram Chat - SSE 模拟服务端

用于本地开发和调试微信小程序的 SSE 流式对话功能。

用法:
  pip install fastapi uvicorn sse-starlette
  python mock-server.py

服务启动后:
  GET  http://0.0.0.0:4000/events  - 流式计数器示例
  POST http://0.0.0.0:4000/chat    - 模拟 AI 聊天（接受 { "prompt": "..." }）

测试:
  curl http://0.0.0.0:4000/events
  curl -X POST "http://0.0.0.0:4000/chat" -H "Content-Type: application/json" -d '{"prompt":"你好"}'
"""

import json
import asyncio
import time
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

app = FastAPI(title="TDesign Chat Mock SSE Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- 通用流式计数器 ----------

async def event_generator():
    """简单的计数器流式示例"""
    count = 0
    while True:
        await asyncio.sleep(1)
        count += 1
        data = {"count": count}
        yield json.dumps(data)


@app.get("/events")
@app.post("/events")
async def get_events():
    return EventSourceResponse(event_generator())


# ---------- 模拟 AI 聊天 ----------

class ChatRequest(BaseModel):
    prompt: str = ""


# 预定义回复库
MOCK_REPLIES = {
    "你好": "你好！我是 TDesign AI 助手，有什么可以帮你的吗？",
    "hello": "Hello! I'm TDesign AI assistant. How can I help you?",
    "默认": (
        "收到你的消息了。作为 TDesign 小程序聊天组件的演示服务端，"
        "我正在模拟流式输出的效果。这段文字会逐字返回，"
        "模拟真实大模型（如混元、GPT 等）的 SSE 响应格式。"
    ),
}

# Markdown 格式回复示例
MARKDOWN_REPLY = """# 欢迎使用 TDesign Chat

## 功能特性

- **流式输出**：支持 SSE 实时推送
- **Markdown 渲染**：完整支持标题、列表、代码块、表格等
- **思考过程**：可展示 AI 推理过程

### 代码示例

```javascript
const sse = createSSEClient({
  url: 'https://your-api-url',
  method: 'POST',
  data: { prompt: '你好' },
  onMessage(content) {
    console.log(content);
  },
});
```

### 表格示例

| 组件 | 用途 | 优先级 |
|:-----|:----:|-------:|
| ChatList | 消息列表 | 高 |
| ChatSender | 输入框 | 高 |
| ChatMessage | 消息体 | 高 |

> 提示：这是模拟服务端返回的 Markdown 内容，用于测试渲染效果。
"""


async def chat_generator(prompt: str):
    """模拟大模型的流式输出"""
    # 选择回复内容
    reply = MOCK_REPLIES.get(prompt.strip())
    if reply is None:
        # 关键词部分匹配
        for key, value in MOCK_REPLIES.items():
            if key in prompt.lower():
                reply = value
                break
        else:
            reply = MARKDOWN_REPLY

    # 模拟逐字流式输出
    request_id = f"chat-{int(time.time() * 1000)}"
    created = int(time.time())

    total_tokens = 0
    prompt_tokens = len(prompt)
    completion_tokens = 0

    for i, char in enumerate(reply):
        await asyncio.sleep(random.uniform(0.02, 0.08))  # 模拟生成延迟

        completion_tokens += 1
        total_tokens = prompt_tokens + completion_tokens

        chunk_data = {
            "id": request_id,
            "created": created,
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "role": "assistant" if i == 0 else None,
                        "content": char,
                    },
                    "finish_reason": None,
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            },
        }

        # 移除值为 None 的字段，保持输出简洁
        choices = chunk_data["choices"][0]
        if choices["delta"].get("role") is None:
            del choices["delta"]["role"]
        if choices.get("finish_reason") is None:
            del choices["finish_reason"]

        yield json.dumps(chunk_data, ensure_ascii=False)

    # 发送结束标记
    yield "[DONE]"


@app.post("/chat")
async def chat(request: ChatRequest):
    """模拟 AI 聊天接口"""
    return EventSourceResponse(chat_generator(request.prompt))


# ---------- 健康检查 ----------

@app.get("/health")
async def health():
    return {"status": "ok", "time": time.time()}


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("TDesign Chat Mock SSE Server")
    print("=" * 50)
    print("服务地址:")
    print("  SSE 计数器:  http://0.0.0.0:4000/events")
    print("  模拟聊天:     http://0.0.0.0:4000/chat  (POST)")
    print("  健康检查:     http://0.0.0.0:4000/health")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=4000)
