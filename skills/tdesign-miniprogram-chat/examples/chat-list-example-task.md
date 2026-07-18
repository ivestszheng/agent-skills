<!--
  文件名: chat-list-example-task.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-list#任务规划
  场景: 任务规划
  描述: 演示 Agent 多步骤任务场景，使用步骤条渲染任务执行过程。
  依赖组件: t-chat-message, t-chat-actionbar, t-chat-sender, t-chat-content, t-steps, t-step-item, t-icon, t-toast
  关键特性: agent内容类型, t-steps步骤条, 多阶段流式
-->

# ChatList 代码演示-任务规划

```wxml
<view class="chat-box" style="height: {{contentHeight}};">
  <t-chat>
    <block wx:for="{{chatList}}" wx:key="chatId" wx:for-index="chatIndex">
      <t-chat-message
        chat-id="{{item.chatId}}"
        avatar="{{item.avatar || ''}}"
        name="{{item.name || ''}}"
        datetime="{{item.datetime || ''}}"
        role="{{item.message.role}}"
        placement="{{item.message.role === 'user' ? 'right' : 'left'}}"
        bind:message-longpress="showPopover"
      >
        <view slot="content">
          <block
            wx:for="{{item.message.content}}"
            wx:for-item="contentItem"
            wx:for-index="contentIndex"
            wx:key="contentIndex"
          >
            <t-chat-content
              content="{{contentItem}}"
              wx:if="{{contentItem.type === 'text' || contentItem.type === 'markdown'}}"
            />
            <view class="step" wx:if="{{contentItem.type === 'agent'}}">
              <t-steps layout="vertical" current="{{contentItem.content.steps.length}}">
                <t-step-item wx:for="{{contentItem.content.steps}}" wx:key="index" title="{{item.step}}">
                  <view slot="content" class="step-text-list">
                    <view
                      wx:for="{{item.tasks}}"
                      wx:key="index"
                      wx:for-item="taskItem"
                      class="step-text {{taskItem.type}}"
                    >
                      <t-icon
                        wx:if="{{taskItem.type === 'command'}}"
                        name="control-platform"
                        size="32rpx"
                        class="step-icon"
                      />
                      {{taskItem.text}}
                    </view>
                  </view>
                </t-step-item>
              </t-steps>
            </view>
          </block>
        </view>
        <t-chat-actionbar
          wx:if="{{chatIndex !== chatList.length - 1 && item.message.status === 'complete' && item.message.role === 'assistant'}}"
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
        renderPresets="{{renderPresets}}"
        bind:send="onSend"
        bind:stop="onStop"
        bind:focus="onFocus"
        autoRiseWithKeyboard="{{true}}"
      />
    </view>
  </t-chat>
  <t-chat-actionbar
    class="popover-actionbar"
    placement="longpress"
    bind:actions="handlePopoverAction"
    longPressPosition="{{longPressPosition}}"
  />
</view>
<t-toast id="t-toast" />

```

```js
import Toast from 'tdesign-miniprogram/toast';
import getNavigationBarHeight from '../utils';

let uniqueId = 0;
const getUniqueKey = () => {
  uniqueId += 1;
  return `key-${uniqueId}`;
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const fetchStream = async (str, options) => {
  const { success, complete, delay = 100 } = options;

  const arr = str.split('');

  for (let i = 0; i < arr.length; i += 1) {
    // eslint-disable-next-line no-await-in-loop
    await sleep(delay);
    success(arr[i]);
  }

  complete();
};

Component({
  properties: {
    contentHeight: {
      type: String,
      value: '100vh',
    },

    isActive: {
      type: Boolean,
      value: false,
      observer: function (v) {
        this.setData({
          value: v ? '请帮我做一个5岁儿童生日聚会的规划' : '', // 输入框的值
        });
      },
    },
  },

  options: {
    styleIsolation: 'shared',
  },
  data: {
    renderPresets: [
      {
        name: 'send',
        type: 'icon',
      },
    ],
    chatList: [
      {
        avatar: 'https://tdesign.gtimg.com/site/chat-avatar.png',
        message: {
          role: 'assistant',
          content: [
            {
              type: 'text',
              data: '欢迎使用TDesign Agent家庭活动策划助手，请给我布置任务吧～',
            },
          ],
        },
        chatId: getUniqueKey(),
      },
    ],
    value: '', // 输入框的值
    loading: false, // 加载状态
    disabled: false, // 禁用状态
    inputStyle: '', // 输入框动态样式
    activePopoverId: '', // 当前打开悬浮actionbar的chatId
    longPressPosition: null, // 长按位置对象
  },

  methods: {
    // 发送消息事件处理
    onSend(e) {
      const { value } = e.detail;
      if (!value || value.trim() === '') return;

      // 创建用户消息对象
      const userMessage = {
        message: {
          role: 'user',
          content: [
            {
              type: 'text',
              data: value.trim(),
            },
          ],
        },
        chatId: getUniqueKey(),
      };

      // 将用户消息插入到chatList的开头（因为reverse为true，所以用unshift）
      this.setData({
        chatList: [userMessage, ...this.data.chatList],
        value: '', // 清空输入框
      });

      // 模拟助手回复（可选）
      this.simulateAssistantReply(value.trim());
    },

    // 停止事件处理
    onStop() {
      console.log('停止发送');
      this.setData({
        loading: false,
      });
    },

    // 聚焦事件处理
    onFocus() {
      console.log('输入框聚焦');
    },

    // 模拟助手回复
    simulateAssistantReply() {
      this.setData({ loading: true });

      const assistantMessage = {
        avatar: 'https://tdesign.gtimg.com/site/chat-avatar.png',
        message: {
          role: 'assistant',
          content: [
            {
              type: 'markdown',
              data: '',
            },
          ],
        },
        chatId: getUniqueKey(),
      };

      this.setData({
        chatList: [assistantMessage, ...this.data.chatList],
      });

      const that = this;
      wx.nextTick(async () => {
        await fetchStream('为5岁小朋友准备一场生日派对，我会根据要求准备合适方案，计划从以下几个步骤进行准备：', {
          success(result) {
            if (!that.data.loading) return;
            that.setData({
              'chatList[0].message.content[0].data': that.data.chatList[0].message.content[0].data + result,
            });
          },
          complete() {},
        });
        if (!that.data.loading) return;

        that.data.chatList[0].message.content.push({
          type: 'agent',
          id: 'task1',
          content: {
            text: '',
            steps: [],
          },
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream('生日聚会规划任务已分解为3个执行阶段', {
          success(result) {
            if (!that.data.loading) return;
            that.setData({
              'chatList[0].message.content[1].content.text':
                that.data.chatList[0].message.content[1].content.text + result,
            });
          },
          complete() {},
        });

        if (!that.data.loading) return;

        that.data.chatList[0].message.content[1].content.steps.push({
          step: '确定派对餐饮方案',
          agent_id: 'a1',
          tasks: [
            {
              type: 'command',
              text: '',
            },
          ],
          status: 'finish',
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream('调用智能搜索工具', {
          success(result) {
            if (!that.data.loading) return;
            that.setData({
              'chatList[0].message.content[1].content.steps[0].tasks[0].text':
                that.data.chatList[0].message.content[1].content.steps[0].tasks[0].text + result,
            });
          },
          complete() {},
        });

        if (!that.data.loading) return;

        that.data.chatList[0].message.content[1].content.steps[0].tasks.push({
          type: 'command',
          text: '',
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream('已筛选出3种高性价比菜单方案，开始进行营养匹配', {
          success(result) {
            if (!that.data.loading) return;
            that.setData({
              'chatList[0].message.content[1].content.steps[0].tasks[1].text':
                that.data.chatList[0].message.content[1].content.steps[0].tasks[1].text + result,
            });
          },
          complete() {},
        });

        if (!that.data.loading) return;

        that.data.chatList[0].message.content[1].content.steps[0].tasks.push({
          type: 'result',
          text: '',
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream('主菜是香草烤鸡（无麸质），准备耗时45分钟；', {
          success(result) {
            if (!that.data.loading) return;
            that.setData({
              'chatList[0].message.content[1].content.steps[0].tasks[2].text':
                that.data.chatList[0].message.content[1].content.steps[0].tasks[2].text + result,
            });
          },
          complete() {},
        });
        if (!that.data.loading) return;

        that.data.chatList[0].message.content[1].content.steps.push({
          step: '准备派对现场布置',
          agent_id: 'a2',
          tasks: [
            {
              type: 'command',
              text: '',
            },
          ],
          status: 'finish',
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream('调用智能搜索工具，搜索儿童派对用品清单', {
          success(result) {
            if (!that.data.loading) return;
            that.setData({
              'chatList[0].message.content[1].content.steps[1].tasks[0].text':
                that.data.chatList[0].message.content[1].content.steps[1].tasks[0].text + result,
            });
          },
          complete() {},
        });

        if (!that.data.loading) return;

        that.data.chatList[0].message.content[1].content.steps[1].tasks.push({
          type: 'result',
          text: '',
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream(
          '推荐现场布置方案：餐具（一次性纸盘、刀叉套装）、杯子、纸巾、一次性桌布，装饰气球、横幅、礼帽等',
          {
            success(result) {
              if (!that.data.loading) return;
              that.setData({
                'chatList[0].message.content[1].content.steps[1].tasks[1].text':
                  that.data.chatList[0].message.content[1].content.steps[1].tasks[1].text + result,
              });
            },
            complete() {},
          },
        );

        if (!that.data.loading) return;

        that.data.chatList[0].message.content[1].content.steps.push({
          step: '策划派对活动',
          agent_id: 'a1',
          tasks: [
            {
              type: 'command',
              text: '',
            },
          ],
          status: 'finish',
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream('搜索儿童派对游戏', {
          success(result) {
            if (!that.data.loading) return;
            that.setData({
              'chatList[0].message.content[1].content.steps[2].tasks[0].text':
                that.data.chatList[0].message.content[1].content.steps[2].tasks[0].text + result,
            });
          },
          complete() {},
        });

        if (!that.data.loading) return;

        that.data.chatList[0].message.content[1].content.steps[2].tasks.push({
          type: 'command',
          text: '',
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream('整理信息并进行合理性分析，安全性评估', {
          success(result) {
            if (!that.data.loading) return;
            that.setData({
              'chatList[0].message.content[1].content.steps[2].tasks[1].text':
                that.data.chatList[0].message.content[1].content.steps[2].tasks[1].text + result,
            });
          },
          complete() {},
        });

        if (!that.data.loading) return;

        that.data.chatList[0].message.content[1].content.steps[2].tasks.push({
          type: 'result',
          text: '',
        });
        that.setData({
          chatList: that.data.chatList,
        });

        await fetchStream(
          '派对总时长建议控制在1.5小时，符合5岁儿童注意力持续时间，每位小朋友到达时可以在拍照区留影，可设置一个签到',
          {
            success(result) {
              if (!that.data.loading) return;
              that.setData({
                'chatList[0].message.content[1].content.steps[2].tasks[2].text':
                  that.data.chatList[0].message.content[1].content.steps[2].tasks[2].text + result,
              });
            },
            complete() {},
          },
        );
        that.setData({
          'chatList[0].message.status': 'complete',
          loading: false,
        });
      });
    },
    handleAction(e) {
      const { name, active, data } = e.detail;

      let message = '';
      switch (name) {
        case 'replay':
          message = '重新生成';
          break;
        case 'copy':
          console.log(data);
          message = '复制成功';
          break;
        case 'good':
          message = active ? '点赞成功' : '取消点赞';
          break;
        case 'bad':
          message = active ? '点踩成功' : '取消点踩';
          break;
        case 'share':
          message = '分享功能';
          break;
        default:
          message = `执行了${name}操作`;
      }

      Toast({
        context: this,
        selector: '#t-toast',
        message,
        theme: 'success',
      });
    },
    showPopover(e) {
      const { id, longPressPosition } = e.detail;

      let role = '';
      this.data.chatList.forEach((item) => {
        if (item.chatId === id) {
          role = item.message.role;
        }
      });

      // 仅当 role 为 user 时才显示 popover
      if (role !== 'user') {
        return;
      }

      this.setData({
        activePopoverId: id,
        longPressPosition,
      });
    },
    handlePopoverAction(e) {
      e.detail.chatId = this.data.activePopoverId;
      this.handleAction(e);
    },
  },
  lifetimes: {
    attached: function () {
      /**
       * 计算内容区域高度
       * 生成CSS calc表达式：calc(100vh - 96rpx - 导航高度 - 底部安全区域高度)
       */
      try {
        // 获取当前的导航栏高度和安全区域高度
        const navigationBarHeight = getNavigationBarHeight() || 0;

        // 生成CSS calc表达式字符串
        const contentHeight = `calc(100vh - 96rpx - ${navigationBarHeight}px)`;

        this.setData({
          contentHeight: contentHeight,
        });

        console.log('内容区域高度CSS表达式:', contentHeight);
      } catch (error) {
        console.error('生成内容高度表达式失败:', error);
        this.setData({
          contentHeight: 'calc(100vh - 96rpx)',
        });
      }
    },
  },
});

```

```css
.chat-box {
  padding-top: 32rpx;
  box-sizing: border-box;
}

.t-chat__list {
  padding: 0 0 0 32rpx;
  box-sizing: border-box;
}
.t-chat-message {
  padding: 0 32rpx;
}

.preview {
  padding: 16rpx;
  display: flex;
  justify-content: space-between;
  border: 1px solid var(--td-component-border);
}

.step {
  padding-top: 24rpx;
}

.step-text-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.step-text {
  text-align: start;
}

.step-text.command {
  padding: 16rpx;
  border-radius: 16rpx;
  background-color: var(--td-bg-color-secondarycontainer);
  display: flex;
  font-size: 28rpx;
  line-height: 44rpx;
  color: var(--td-text-color-secondary);
}

.step-text.result {
  font-size: 28rpx;
  line-height: 44rpx;
  color: var(--td-text-color-primary);
}

.step-icon {
  margin-right: 12rpx;
  margin-top: 6rpx;
}

.t-steps-item__circle--finish {
  background-color: transparent;
  color: var(--td-text-color-primary);
  border: 1px solid var(--td-text-color-primary);
  width: 16px;
  height: 16px;
}

.t-steps-item__circle--finish .t-icon {
  font-size: 12px;
}

.t-steps-item__line--finish {
  background-color: var(--td-component-border);
}

.t-steps-item__title--finish {
  color: var(--td-text-color-primary);
  font-weight: 600;
}

```

```json
{
  "component": true,
  "styleIsolation": "shared",
  "usingComponents": {
    "t-chat-message": "tdesign-miniprogram/chat-message/chat-message",
    "t-chat-content": "tdesign-miniprogram/chat-content/chat-content",
    "t-chat": "tdesign-miniprogram/chat-list/chat-list",
    "t-chat-sender": "tdesign-miniprogram/chat-sender/chat-sender",
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar",
    "t-steps": "tdesign-miniprogram/steps/steps",
    "t-step-item": "tdesign-miniprogram/step-item/step-item",
    "t-icon": "tdesign-miniprogram/icon/icon",
    "t-toast": "tdesign-miniprogram/toast/toast"
  }
}

```