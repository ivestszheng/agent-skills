# SSE 流式输出接入

## 什么是流式输出

流式输出（Server-Sent Events）指服务器持续将数据推送到客户端，而非一次性发送完毕。连接建立后，服务器可实时发送更新。

### 与普通请求的区别

| 特性 | 普通 HTTP 请求 | SSE 流式请求 |
|------|---------------|-------------|
| 模型 | 请求-响应（一次性） | 持续推送 |
| 连接 | 处理完毕即关闭 | 保持开放，连续发送 |
| 适用 | 普通数据获取 | 实时消息、LLM 生成 |

### 使用场景

- 实时消息推送
- 股票行情更新
- LLM 大模型逐字输出（最常见场景）
- 任何需要服务器向客户端实时传输数据的场合

## 为什么 LLM 需要 SSE

Transformer 推理是逐步生成内容的，推理时间长且有 Max Token 限制。默认采用流式输出包裹，逐段返回更符合用户体验。

## 微信小程序接入 SSE

### 请求方式

```javascript
const requestTask = wx.request({
  url: 'https://your-api-url',
  method: 'POST',
  enableChunked: true,    // 关键：启用分块传输
  header: { 'Content-Type': 'application/json' },
  data: { prompt: '你的问题' },
  success(res) {
    console.log('success:', res);
  },
  fail(err) {
    console.warn('fail:', err);
  },
});

// 解析流式返回的数据
requestTask.onChunkReceived((chunk) => {
  // chunk.data 是 ArrayBuffer，需解码
  const decoder = new TextDecoder('utf-8');
  const text = decoder.decode(chunk.data);

  // 解析 SSE 格式: "data: {...}\n\n"
  const lines = text.split('\n');
  lines.forEach((line) => {
    if (line.startsWith('data: ')) {
      const jsonStr = line.slice(6);
      try {
        const parsed = JSON.parse(jsonStr);
        const content = parsed.choices?.[0]?.delta?.content || '';
        if (content) {
          // 将 content 追加到当前助手消息
          this.appendStreamContent(content);
        }
      } catch (e) {
        // 忽略解析失败的行
      }
    }
  });
});
```

### 服务端 SSE 示例（Python + FastAPI）

```python
import json
import asyncio
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

async def event_generator():
    count = 0
    while True:
        await asyncio.sleep(1)
        count += 1
        data = {"count": count}
        yield json.dumps(data)

@app.post("/events")
async def post_events():
    return EventSourceResponse(event_generator())
```

### LLM 流式返回格式

以混元大模型为例，每次 chunk 返回格式：

```
data: {"id":"xxx","created":1695218378,"choices":[{"delta":{"role":"assistant","content":"我是"}}],"usage":{"prompt_tokens":10,"completion_tokens":1,"total_tokens":11}}

data: {"id":"xxx","created":1695218378,"choices":[{"delta":{"role":"assistant","content":"由腾"}}],"usage":{"prompt_tokens":10,"completion_tokens":3,"total_tokens":13}}
```

组件只关心 `choices[0].delta.content` 字段，将其拼接即可得到完整回复。

## 在 ChatList 中实现流式更新

```javascript
// 1. 创建 pending 状态的助手消息
const assistantMessage = {
  role: 'assistant',
  content: [{ type: 'markdown', data: '' }],
  avatar: 'https://tdesign.gtimg.com/site/chat-avatar.png',
  status: 'pending',
  chatId: getUniqueKey(),
};
this.setData({ chatList: [assistantMessage, ...this.data.chatList] });

// 2. 发起 SSE 请求
const requestTask = wx.request({
  url: 'https://your-llm-api',
  method: 'POST',
  enableChunked: true,
  data: { prompt: userInput },
});

requestTask.onChunkReceived((chunk) => {
  const decoder = new TextDecoder('utf-8');
  const text = decoder.decode(chunk.data);
  const lines = text.split('\n');

  lines.forEach((line) => {
    if (line.startsWith('data: ')) {
      try {
        const parsed = JSON.parse(line.slice(6));
        const delta = parsed.choices?.[0]?.delta?.content || '';
        if (delta) {
          // 追加到助手消息内容
          const chatList = this.data.chatList;
          const msgIndex = chatList.findIndex(m => m.chatId === assistantMessage.chatId);
          if (msgIndex !== -1) {
            const msg = chatList[msgIndex];
            msg.content[0].data += delta;
            this.setData({ chatList });
          }
        }
      } catch (e) { /* ignore */ }
    }
  });
});

// 3. 请求完成后更新状态
requestTask.onComplete(() => {
  const chatList = this.data.chatList;
  const msgIndex = chatList.findIndex(m => m.chatId === assistantMessage.chatId);
  if (msgIndex !== -1) {
    chatList[msgIndex].status = 'complete';
    this.setData({ chatList, loading: false });
  }
});
```
