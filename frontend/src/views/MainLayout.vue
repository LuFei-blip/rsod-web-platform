<template>
  <div class="main-layout">
    <el-container class="layout-container">
      <el-aside width="220px">
        <Sidebar />
      </el-aside>
      <el-container>
        <el-header height="60px">
          <Header />
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
import Header from '../components/Header.vue'
</script>

<style scoped>
.main-layout {
  height: 100vh;
  overflow: hidden;
}

.layout-container {
  height: 100%;
}

.el-aside {
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  overflow: hidden;
}

.el-header {
  padding: 0;
  background: #ffffff;
}

.el-main {
  background: #f5f7fa;
  padding: 0;
  overflow-y: auto;
}
</style>
