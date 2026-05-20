<template>
  <div class="sidebar-container">
    <div class="logo-section">
      <div class="logo-icon">
        <Monitor style="color: white; font-size: 20px" />
      </div>
      <div class="logo-text">
        <div class="logo-title">遥感目标识别平台</div>
        <div class="logo-subtitle">多场景影像·精准识别</div>
      </div>
    </div>

    <div class="nav-menu">
      <div
        v-for="item in menuList"
        :key="item.path"
        class="nav-item"
        :class="{ active: currentPath === item.path }"
        @click="handleMenuClick(item)"
      >
        <el-icon :size="18" class="nav-icon"><component :is="item.icon" /></el-icon>
        <span class="nav-text">{{ item.name }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import {
  Monitor,
  Picture,
  Clock,
  ChatDotRound,
  DataLine,
  User,
} from "@element-plus/icons-vue";

const router = useRouter();
const route = useRoute();

interface MenuItem {
  name: string;
  icon: any;
  path: string;
}

const menuList: MenuItem[] = [
  {
    name: "智能检测",
    icon: Picture,
    path: "/detection",
  },
  {
    name: "历史记录",
    icon: Clock,
    path: "/history",
  },
  {
    name: "AI 问答",
    icon: ChatDotRound,
    path: "/qa",
  },
  {
    name: "目标库",
    icon: DataLine,
    path: "/targets",
  },
  {
    name: "个人中心",
    icon: User,
    path: "/profile",
  },
];

const currentPath = computed(() => route.path);

const handleMenuClick = (item: MenuItem) => {
  router.push(item.path);
};
</script>

<style scoped>
.sidebar-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

.logo-section {
  height: 72px;
  display: flex;
  align-items: center;
  padding: 0 12px;
  border-bottom: 1px solid #e5e7eb;
}

.logo-icon {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  flex-shrink: 0;
}

.logo-text {
  overflow: hidden;
}

.logo-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.3;
  white-space: nowrap;
}

.logo-subtitle {
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
  line-height: 1.3;
  white-space: nowrap;
}

.nav-menu {
  flex: 1;
  padding: 16px 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  flex-direction: row;
  padding: 16px 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background-color: #f0fdf4;
}

.nav-item.active {
  background-color: #f0fdf4;
  border-left: 3px solid #27ae60;
  color: #27ae60;
  font-weight: 500;
}

.nav-item.active .nav-icon {
  color: #27ae60;
}

.nav-icon {
  font-size: 18px;
  margin-right: 12px;
  color: #6b7280;
  flex-shrink: 0;
}

.nav-text {
  font-size: 14px;
  line-height: 1.4;
  color: #1f2937;
}

.nav-item.active .nav-text {
  color: #27ae60;
}
</style>
