<template>
  <div class="qa-page">
    <div class="page-header">
      <div class="breadcrumb">
        <span>工作台</span>
        <span class="separator">›</span>
        <span class="active">AI 问答</span>
      </div>
      <h1 class="page-title">AI 智能问答</h1>
      <p class="page-subtitle">关于遥感目标检测的问题，随时问我</p>
    </div>

    <div class="qa-container">
      <!-- 聊天消息列表 -->
      <div class="message-list" ref="messageListRef">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="message-item"
          :class="msg.role"
        >
          <div class="message-avatar">
            <el-avatar :size="36" :style="{ background: msg.role === 'user' ? '#27ae60' : '#409eff' }">
              {{ msg.role === 'user' ? 'U' : 'AI' }}
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="message-text">{{ msg.content }}</div>
            <div class="message-time">{{ msg.time }}</div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 4 }"
          placeholder="请输入您的问题，例如：这个模型支持哪些目标类型？"
          @keyup.enter.exact="sendMessage"
        />
        <div class="input-actions">
          <span class="tip-text">按 Enter 发送，Shift+Enter 换行</span>
          <el-button type="primary" @click="sendMessage" :loading="sending">
            <el-icon><Promotion /></el-icon>
            发送
          </el-button>
        </div>
      </div>
    </div>

    <!-- 快捷问题 -->
    <div class="quick-questions">
      <span class="quick-label">快捷问题：</span>
      <el-button
        v-for="q in quickQuestions"
        :key="q"
        size="small"
        round
        @click="inputMessage = q"
      >
        {{ q }}
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from "vue";
import { Promotion } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

interface Message {
  role: "user" | "ai";
  content: string;
  time: string;
}

const messages = ref<Message[]>([
  {
    role: "ai",
    content: "你好！我是遥感检测 AI 助手，有什么可以帮助你的吗？",
    time: new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" }),
  },
]);

const inputMessage = ref("");
const sending = ref(false);
const messageListRef = ref<HTMLElement>();

const quickQuestions = [
  "这个模型支持哪些目标类型？",
  "如何提高检测精度？",
  "支持哪些图片格式？",
  "批量检测有什么限制？",
];

const getCurrentTime = () => {
  return new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
};

const scrollToBottom = async () => {
  await nextTick();
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight;
  }
};

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return;

  const userMsg: Message = {
    role: "user",
    content: inputMessage.value.trim(),
    time: getCurrentTime(),
  };
  messages.value.push(userMsg);
  const question = inputMessage.value;
  inputMessage.value = "";
  await scrollToBottom();

  sending.value = true;
  // 模拟AI回复
  setTimeout(() => {
    const aiMsg: Message = {
      role: "ai",
      content: `关于"${question}"的问题：目前该功能正在开发中，敬请期待。`,
      time: getCurrentTime(),
    };
    messages.value.push(aiMsg);
    sending.value = false;
    scrollToBottom();
  }, 1000);
};
</script>

<style scoped>
.qa-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100%;
}

.page-header {
  margin-bottom: 24px;
}

.breadcrumb {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 8px;
}

.breadcrumb .separator {
  margin: 0 4px;
}

.breadcrumb .active {
  color: #27ae60;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px;
}

.page-subtitle {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
}

.qa-container {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 280px);
  min-height: 500px;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
  margin: 0 12px;
}

.message-content {
  max-width: 70%;
}

.message-item.user .message-content {
  text-align: right;
}

.message-text {
  background: #f0fdf4;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  color: #1f2937;
  display: inline-block;
}

.message-item.user .message-text {
  background: #27ae60;
  color: #ffffff;
}

.message-time {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

.input-area {
  border-top: 1px solid #e5e7eb;
  padding-top: 16px;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.tip-text {
  font-size: 12px;
  color: #9ca3af;
}

.quick-questions {
  margin-top: 16px;
  background: #ffffff;
  padding: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.quick-label {
  font-size: 13px;
  color: #6b7280;
  margin-right: 8px;
}
</style>
