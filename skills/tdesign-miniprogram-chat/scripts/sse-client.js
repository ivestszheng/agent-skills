/**
 * TDesign Miniprogram Chat - SSE 客户端封装
 *
 * 用法：在页面/组件中 import 此模块，调用 createSSEClient 创建实例
 *
 * ```javascript
 * import { createSSEClient } from '../../scripts/sse-client';
 *
 * const sse = createSSEClient({
 *   url: 'https://your-api-url',
 *   method: 'POST',
 *   data: { prompt: '你好' },
 *   onMessage(content) {
 *     // 每次收到增量内容
 *     this.appendStreamContent(content);
 *   },
 *   onComplete() {
 *     // 流式结束
 *     this.setData({ loading: false });
 *   },
 *   onError(err) {
 *     console.error('SSE error:', err);
 *   },
 * });
 *
 * // 停止请求
 * sse.abort();
 * ```
 */

/**
 * 创建 SSE 客户端
 * @param {Object} options 配置项
 * @param {string} options.url - 请求地址
 * @param {'GET'|'POST'} [options.method='POST'] - 请求方法
 * @param {Object} [options.header] - 请求头
 * @param {Object} [options.data] - 请求数据
 * @param {Function} [options.onMessage] - 收到增量内容回调 (content: string) => void
 * @param {Function} [options.onComplete] - 流式结束回调 () => void
 * @param {Function} [options.onError] - 错误回调 (err: any) => void
 * @param {Function} [options.onChunk] - 原始 chunk 回调 (chunk: any) => void
 * @param {string} [options.contentPath='choices.0.delta.content'] - 从 JSON 中提取内容的字段路径
 * @returns {{ abort: Function }} 返回包含 abort 方法的对象
 */
function createSSEClient(options) {
  const {
    url,
    method = 'POST',
    header = {},
    data = {},
    onMessage,
    onComplete,
    onError,
    onChunk,
    contentPath = 'choices.0.delta.content',
  } = options;

  // 解析嵌套字段路径，如 "choices.0.delta.content"
  function getNestedValue(obj, path) {
    return path.split('.').reduce((acc, key) => {
      if (acc === null || acc === undefined) return null;
      return acc[key];
    }, obj);
  }

  // 解码 ArrayBuffer 并解析 SSE 格式
  function parseSSEChunk(chunk) {
    try {
      const decoder = new TextDecoder('utf-8');
      const text = decoder.decode(chunk.data);
      const lines = text.split('\n');

      lines.forEach((line) => {
        // SSE 标准格式：data: {...}
        const trimmed = line.trim();
        if (trimmed.startsWith('data: ')) {
          const jsonStr = trimmed.slice(6);

          // 跳过 [DONE] 标记
          if (jsonStr === '[DONE]') {
            if (onComplete) onComplete();
            return;
          }

          try {
            const parsed = JSON.parse(jsonStr);
            const content = getNestedValue(parsed, contentPath);

            if (content && onMessage) {
              onMessage(content);
            }
          } catch (e) {
            // 忽略非 JSON 行
          }
        }
      });
    } catch (e) {
      if (onError) onError(e);
    }
  }

  // 发起请求
  const requestTask = wx.request({
    url,
    method,
    header: {
      'Content-Type': 'application/json',
      ...header,
    },
    data,
    enableChunked: true,
    success(res) {
      // 非流式响应的 success（enableChunked 下通常不会触发）
      if (onComplete) onComplete();
    },
    fail(err) {
      if (onError) onError(err);
    },
  });

  // 监听分块数据
  requestTask.onChunkReceived((chunk) => {
    if (onChunk) onChunk(chunk);
    parseSSEChunk(chunk);
  });

  // 返回可中止的控制器
  return {
    abort() {
      requestTask.abort();
    },
  };
}

/**
 * 生成唯一 ID
 * @param {string} [prefix='msg'] - 前缀
 * @returns {string}
 */
function generateId(prefix = 'msg') {
  return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

/**
 * 创建助手消息对象
 * @param {Object} options
 * @param {string} [options.avatar='https://tdesign.gtimg.com/site/chat-avatar.png']
 * @returns {Object}
 */
function createAssistantMessage(options = {}) {
  return {
    role: 'assistant',
    content: [{ type: 'markdown', data: '' }],
    avatar: options.avatar || 'https://tdesign.gtimg.com/site/chat-avatar.png',
    name: options.name || 'AI 助手',
    status: 'pending',
    chatId: generateId('assistant'),
    datetime: '',
  };
}

/**
 * 创建用户消息对象
 * @param {string} text - 用户输入文本
 * @returns {Object}
 */
function createUserMessage(text) {
  return {
    role: 'user',
    content: [{ type: 'text', data: text }],
    chatId: generateId('user'),
    datetime: '',
  };
}

module.exports = {
  createSSEClient,
  generateId,
  createAssistantMessage,
  createUserMessage,
};
