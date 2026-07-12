/**
 * TDesign Miniprogram Chat - 聊天页面模板生成器
 *
 * 运行: node create-chat-page.js <页面路径>
 * 示例: node create-chat-page.js pages/chat/chat
 *
 * 会在指定路径下生成完整聊天页面的 4 个文件：
 *   - <path>.wxml
 *   - <path>.wxss
 *   - <path>.js
 *   - <path>.json
 */

const fs = require('fs');
const path = require('path');

// 获取命令行参数
const targetPath = process.argv[2];

if (!targetPath) {
  console.error('用法: node create-chat-page.js <页面路径>');
  console.error('示例: node create-chat-page.js pages/chat/chat');
  process.exit(1);
}

// 确保目录存在
const dir = path.dirname(targetPath);
if (!fs.existsSync(dir)) {
  fs.mkdirSync(dir, { recursive: true });
}

// ========== WXML 模板 ==========
const wxml = `<view class="chat-box" style="height: {{contentHeight}};">
  <t-chat id="chatList" bindscroll="onScroll">
    <block wx:for="{{chatList}}" wx:key="chatId">
      <t-chat-message
        chat-id="{{item.chatId}}"
        avatar="{{item.avatar || ''}}"
        name="{{item.name || ''}}"
        datetime="{{item.datetime || ''}}"
        content="{{item.content}}"
        role="{{item.role}}"
        placement="{{item.role === 'user' ? 'right' : 'left'}}"
        status="{{item.status || ''}}"
        bind:message-longpress="showPopover"
        bind:click="onClick"
      >
        <t-chat-actionbar
          wx:if="{{index !== chatList.length - 1 && item.status === 'complete' && item.role === 'assistant'}}"
          id="{{'actionbar-' + item.chatId}}"
          chat-id="{{item.chatId}}"
          comment="{{item.comment}}"
          slot="actionbar"
          placement="end"
          bind:actions="handleAction"
        />
      </t-chat-message>
    </block>
    <view slot="footer">
      <t-chat-sender
        value="{{value}}"
        loading="{{loading}}"
        disabled="{{disabled}}"
        autoRiseWithKeyboard="{{true}}"
        renderPresets="{{renderPresets}}"
        bind:send="onSend"
        bind:stop="onStop"
        bind:focus="onFocus"
      />
    </view>
  </t-chat>
</view>

<t-toast id="t-toast" />
`;

// ========== WXSS 模板 ==========
const wxss = `.chat-box {
  display: flex;
  flex-direction: column;
  background-color: var(--td-bg-color-container, #fff);
}
`;

// ========== JS 模板 ==========
const js = `/**
 * 聊天页面
 * 基于 TDesign Miniprogram Chat 组件
 *
 * 使用前请确保:
 * 1. 已安装 tdesign-miniprogram: npm i tdesign-miniprogram -S
 * 2. 已在微信开发者工具中构建 npm
 * 3. 已移除 app.json 中的 "style": "v2"
 */

const { createSSEClient, generateId, createAssistantMessage, createUserMessage } =
  require('../../scripts/sse-client');

const ASSISTANT_AVATAR = 'https://tdesign.gtimg.com/site/chat-avatar.png';

Component({
  options: {
    styleIsolation: 'shared',
  },

  data: {
    chatList: [],
    value: '',
    loading: false,
    disabled: false,
    contentHeight: '100vh',
    renderPresets: [{ name: 'send', type: 'icon' }],
    activePopoverId: '',
    longPressPosition: null,
    // 当前 SSE 请求引用（用于中止）
    _currentSSE: null,
  },

  lifetimes: {
    attached() {
      // 计算内容区域高度
      const systemInfo = wx.getSystemInfoSync();
      const contentHeight = systemInfo.windowHeight + 'px';
      this.setData({ contentHeight });

      // 添加欢迎消息
      const welcomeMsg = {
        role: 'assistant',
        content: [{ type: 'text', data: '你好！有什么可以帮你的？' }],
        avatar: ASSISTANT_AVATAR,
        status: 'complete',
        chatId: generateId('welcome'),
        datetime: this._formatTime(new Date()),
      };
      this.setData({ chatList: [welcomeMsg] });
    },
  },

  methods: {
    // ===== 发送消息 =====
    onSend(e) {
      const { value } = e.detail;
      if (!value || value.trim() === '') return;

      const text = value.trim();

      // 1. 创建用户消息
      const userMessage = createUserMessage(text);
      userMessage.datetime = this._formatTime(new Date());

      // 2. 创建助手占位消息
      const assistantMessage = createAssistantMessage({ avatar: ASSISTANT_AVATAR });
      assistantMessage.datetime = this._formatTime(new Date());

      // 3. 更新列表
      this.setData({
        chatList: [assistantMessage, userMessage, ...this.data.chatList],
        value: '',
        loading: true,
        disabled: true,
      });

      // 4. 发起 SSE 请求
      this._requestSSE(text, assistantMessage.chatId);
    },

    // ===== SSE 请求 =====
    _requestSSE(prompt, assistantChatId) {
      const that = this;

      // 中止之前的请求
      if (this.data._currentSSE) {
        this.data._currentSSE.abort();
      }

      const sse = createSSEClient({
        url: 'https://your-api-url/chat', // 替换为你的 API 地址
        method: 'POST',
        data: { prompt },
        onMessage(content) {
          that._appendStreamContent(content, assistantChatId);
        },
        onComplete() {
          that._completeStream(assistantChatId);
        },
        onError(err) {
          console.error('SSE Error:', err);
          that._completeStream(assistantChatId, 'error');
        },
      });

      this.data._currentSSE = sse;
    },

    // ===== 追加流式内容 =====
    _appendStreamContent(content, chatId) {
      const chatList = this.data.chatList;
      const msgIndex = chatList.findIndex((m) => m.chatId === chatId);
      if (msgIndex !== -1) {
        const msg = chatList[msgIndex];
        msg.content[0].data += content;
        this.setData({ chatList });
        wx.nextTick(() => this.scrollToBottom());
      }
    },

    // ===== 完成流式 =====
    _completeStream(chatId, status = 'complete') {
      const chatList = this.data.chatList;
      const msgIndex = chatList.findIndex((m) => m.chatId === chatId);
      if (msgIndex !== -1) {
        chatList[msgIndex].status = status;
        this.setData({
          chatList,
          loading: false,
          disabled: false,
          _currentSSE: null,
        });
      }
    },

    // ===== 停止生成 =====
    onStop() {
      if (this.data._currentSSE) {
        this.data._currentSSE.abort();
        this.data._currentSSE = null;
      }
      this.setData({ loading: false, disabled: false });

      // 将最后一条助手消息标记为 complete
      const chatList = this.data.chatList;
      for (let i = 0; i < chatList.length; i++) {
        if (chatList[i].role === 'assistant' && chatList[i].status === 'pending') {
          chatList[i].status = 'complete';
          break;
        }
      }
      this.setData({ chatList });
    },

    // ===== 滚动到底部 =====
    scrollToBottom() {
      const chatListComponent = this.selectComponent('#chatList');
      if (chatListComponent && typeof chatListComponent.scrollToBottom === 'function') {
        chatListComponent.scrollToBottom();
      }
    },

    // ===== 聚焦 =====
    onFocus() {
      // 输入框聚焦时的处理
    },

    // ===== 滚动监听 =====
    onScroll(e) {
      // console.log('scroll:', e);
    },

    // ===== 消息点击 =====
    onClick(e) {
      // console.log('click:', e);
    },

    // ===== 长按弹出操作栏 =====
    showPopover(e) {
      const { chatId } = e.currentTarget.dataset;
      this.setData({ activePopoverId: chatId });
    },

    // ===== 操作栏事件 =====
    handleAction(e) {
      const { action, chatId } = e.detail;
      const chatList = this.data.chatList;
      const msg = chatList.find((m) => m.chatId === chatId);
      if (!msg) return;

      const text = msg.content.map((c) => c.data).join('');

      switch (action) {
        case 'copy':
          wx.setClipboardData({ data: text });
          break;
        case 'quote':
          this.setData({ value: text });
          break;
        case 'share':
          // 分享逻辑
          break;
      }
    },

    // ===== 工具方法 =====
    _formatTime(date) {
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return hours + ':' + minutes;
    },
  },
});
`;

// ========== JSON 模板 ==========
const json = `{
  "component": true,
  "usingComponents": {
    "t-chat": "tdesign-miniprogram/chat-list/chat-list",
    "t-chat-message": "tdesign-miniprogram/chat-message/chat-message",
    "t-chat-sender": "tdesign-miniprogram/chat-sender/chat-sender",
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar",
    "t-toast": "tdesign-miniprogram/toast/toast"
  }
}
`;

// ========== 写入文件 ==========
const files = {
  [targetPath + '.wxml']: wxml,
  [targetPath + '.wxss']: wxss,
  [targetPath + '.js']: js,
  [targetPath + '.json']: json,
};

for (const [filePath, content] of Object.entries(files)) {
  fs.writeFileSync(filePath, content, 'utf-8');
  console.log(`已创建: ${filePath}`);
}

console.log('\n聊天页面模板生成完成！');
console.log('请记得:');
console.log('  1. 将 sse-client.js 复制到项目 scripts 目录');
console.log('  2. 替换 JS 中的 API 地址为你的实际后端地址');
console.log('  3. 在 app.json 中注册新页面路径');
