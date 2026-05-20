<template>
  <div class="header-container">
    <div class="header-left">
      <span class="page-title">{{ currentPageName }}</span>
    </div>
    <div class="header-right">
      <el-dropdown trigger="click" @command="handleCommand">
        <span class="user-dropdown">
          <el-avatar :size="32" style="background: #27ae60; margin-right: 8px;">
            {{ username.charAt(0).toUpperCase() }}
          </el-avatar>
          <span class="username">{{ username }}</span>
          <el-icon><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人中心</el-dropdown-item>
            <el-dropdown-item command="settings">设置</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ArrowDown } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

const route = useRoute();
const router = useRouter();

const currentPageName = computed(() => {
  return (route.meta.title as string) || route.name as string || "";
});

const username = computed(() => {
  return localStorage.getItem("username") || "用户";
});

const handleCommand = (command: string) => {
  switch (command) {
    case "profile":
      router.push("/profile");
      break;
    case "settings":
      ElMessage.info("设置功能开发中");
      break;
    case "logout":
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      ElMessage.success("已退出登录");
      router.push("/login");
      break;
  }
};
</script>

<style scoped>
.header-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.user-dropdown:hover {
  background: #f3f4f6;
}

.username {
  font-size: 14px;
  color: #1f2937;
  margin-right: 4px;
}
</style>
