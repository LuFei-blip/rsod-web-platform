<template>
  <div class="detection-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="breadcrumb">
        <span>工作台</span>
        <span class="separator">›</span>
        <span class="active">智能检测</span>
      </div>
      <h1 class="page-title">上传遥感影像，立即识别多类目标</h1>
      <p class="page-subtitle">
        支持飞机 / 油罐 / 操场 / 建筑物 / 船舶 / 农业虫害等多目标检测
      </p>
    </div>

    <!-- 模型选择器 -->
    <div class="model-selector">
      <span class="model-label">检测模型：</span>
      <el-select v-model="selectedModel" style="width: 180px">
        <el-option label="pest-v1" value="pest-v1" />
        <el-option label="pest-v2" value="pest-v2" />
      </el-select>
    </div>

    <!-- 功能选项卡 -->
    <div class="function-tabs">
      <div
        v-for="tab in functionTabs"
        :key="tab.key"
        class="function-tab"
        :class="{ active: activeTab === tab.key }"
        :data-key="tab.key"
        @click="handleTabClick(tab.key)"
      >
        <input
          type="file"
          :accept="tab.accept"
          :multiple="tab.multiple"
          class="file-input"
          @change="handleFileChange($event, tab.key)"
          @click.stop
        />
        <el-icon :size="18" class="tab-icon"><component :is="tab.icon" /></el-icon>
        <div class="tab-content">
          <span class="tab-text">{{ tab.name }}</span>
          <span class="tab-desc">{{ tab.desc }}</span>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧检测结果区域 -->
      <div class="left-panel">
        <div class="panel-header">
          <span class="panel-title">检测预览</span>
          <el-tag v-if="detectionResult" type="success" effect="light" class="result-tag">
            <el-icon class="el-icon--left"><Check /></el-icon>
            检测完成
          </el-tag>
        </div>

        <!-- 工具栏 -->
        <div class="toolbar">
          <el-button
            :class="{ active: compareMode === 'side' }"
            size="small"
            @click="compareMode = 'side'"
          >
            <el-icon><Minus /></el-icon>
            并排对比
          </el-button>
          <el-button
            :class="{ active: compareMode === 'grid' }"
            size="small"
            @click="compareMode = 'grid'"
          >
            <el-icon><Grid /></el-icon>
            栅格对比
          </el-button>
        </div>

        <!-- 图片对比区域 -->
        <div class="image-compare" :class="compareMode">
          <div class="image-card">
            <img
              v-if="originalImage"
              :src="originalImage"
              alt="原始图片"
              class="compare-image"
            />
            <el-empty v-else description="请上传图片" :image-size="120" />
            <div class="image-label">原始图片</div>
          </div>
          <div class="image-card">
            <img
              v-if="resultImage"
              :src="resultImage"
              alt="检测结果"
              class="compare-image"
            />
            <el-empty v-else description="等待检测结果" :image-size="120" />
            <div class="image-label">检测结果</div>
          </div>
        </div>
      </div>

      <!-- 右侧信息面板 -->
      <div class="right-panel">
        <!-- 模型信息 -->
        <div class="info-card">
          <div class="info-item">
            <span class="info-label">检测模型</span>
            <span class="info-value">{{ selectedModel }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">模型版本</span>
            <span class="info-value">v1.0.0</span>
          </div>
        </div>

        <!-- 识别清单 -->
        <div class="result-card">
          <div class="card-header">
            <el-icon><List /></el-icon>
            <span class="card-title">识别清单</span>
          </div>
          <div v-if="!detectionResult || detectionResult.total_objects === 0" class="empty-state">
            <el-icon class="empty-icon"><CircleCheck /></el-icon>
            <p class="empty-text">未检测到目标</p>
            <p class="empty-desc">影像无异常目标</p>
          </div>
          <div v-else class="detection-list">
            <div
              v-for="(box, index) in detectionResult.boxes"
              :key="index"
              class="detection-item"
            >
              <span class="item-name">{{ box.class_name }}</span>
              <span class="item-confidence">{{ (box.confidence * 100).toFixed(1) }}%</span>
            </div>
          </div>
        </div>

        <!-- AI诊断建议 -->
        <div class="result-card">
          <div class="card-header">
            <el-icon><ChatDotRound /></el-icon>
            <span class="card-title">AI 诊断建议</span>
          </div>
          <div class="diagnosis-content">
            <p v-if="!detectionResult">未检测到指定目标</p>
            <p v-else>
              检测到 {{ detectionResult.total_objects }} 个目标，耗时 {{ detectionResult.detection_time }}s。
              模型: {{ detectionResult.model_name }}
            </p>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button size="default" class="btn-secondary" @click="handleRedetect">
            <el-icon><Refresh /></el-icon>
            重新检测
          </el-button>
          <el-button type="primary" size="default" class="btn-primary">
            查看完整报告
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage, ElLoading } from "element-plus";
import {
  Picture,
  Plus,
  Folder,
  Monitor,
  Check,
  Grid,
  List,
  CircleCheck,
  ChatDotRound,
  Refresh,
  Minus,
} from "@element-plus/icons-vue";
import { detectSingleImage, type DetectionResult } from "../api/detection";

const selectedModel = ref("pest-v1");
const activeTab = ref("single");
const compareMode = ref<"side" | "grid">("side");
const originalImage = ref("");
const resultImage = ref("");
const detectionResult = ref<DetectionResult | null>(null);
const isDetecting = ref(false);

const functionTabs = [
  {
    key: "single",
    name: "单图检测",
    desc: "快速识别一张图片",
    icon: Picture,
    accept: "image/*",
    multiple: false,
  },
  {
    key: "batch",
    name: "批量检测",
    desc: "一次处理多张图片",
    icon: Plus,
    accept: "image/*",
    multiple: true,
  },
  {
    key: "folder",
    name: "文件夹",
    desc: "上传整个文件夹",
    icon: Folder,
    accept: "image/*",
    multiple: true,
  },
  {
    key: "video",
    name: "视频检测",
    desc: "上传视频自动分析",
    icon: Monitor,
    accept: "video/*",
    multiple: false,
  },
];

const handleTabClick = (key: string) => {
  activeTab.value = key;
  const input = document.querySelector(`.function-tab[data-key="${key}"] .file-input`) as HTMLInputElement;
  if (input) {
    input.click();
  }
};

const handleFileChange = async (event: Event, tabKey: string) => {
  event.stopPropagation();
  event.preventDefault();
  const files = (event.target as HTMLInputElement).files;
  if (files && files.length > 0) {
    if (tabKey === "single") {
      await performSingleDetection(files[0]);
    } else {
      ElMessage.info(`${tabKey}功能开发中`);
    }
  }
  setTimeout(() => {
    (event.target as HTMLInputElement).value = '';
  }, 0);
};

const performSingleDetection = async (file: File) => {
  const loading = ElLoading.service({
    lock: true,
    text: "正在检测中...",
    background: "rgba(0, 0, 0, 0.7)",
  });

  try {
    isDetecting.value = true;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("model_name", selectedModel.value);

    originalImage.value = URL.createObjectURL(file);

    const response = await detectSingleImage(formData);
    if (response.success && response.data) {
      detectionResult.value = response.data;
      // 拼接后端基础URL
      const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api';
      resultImage.value = baseUrl + response.data.result_image_url;
      ElMessage.success("检测成功！");
    } else {
      ElMessage.error(response.message || "检测失败");
    }
  } catch (error: any) {
    console.error("检测错误:", error);
    ElMessage.error("检测失败，请稍后重试");
  } finally {
    isDetecting.value = false;
    loading.close();
  }
};

const handleRedetect = () => {
  const input = document.querySelector(`.function-tab[data-key="single"] .file-input`) as HTMLInputElement;
  if (input) {
    input.click();
  }
};
</script>

<style scoped>
.detection-page {
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

.model-selector {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.model-label {
  font-size: 14px;
  color: #1f2937;
  margin-right: 8px;
}

.function-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.function-tab {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: #ffffff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.function-tab:hover {
  border-color: #27ae60;
}

.function-tab.active {
  background: #f0fdf4;
  border-color: #27ae60;
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  cursor: pointer;
}

.tab-icon {
  margin-right: 8px;
  color: #6b7280;
}

.function-tab.active .tab-icon {
  color: #27ae60;
}

.tab-content {
  display: flex;
  flex-direction: column;
}

.tab-text {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.tab-desc {
  font-size: 12px;
  color: #6b7280;
}

.main-content {
  display: flex;
  gap: 20px;
}

.left-panel {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.panel-title {
  font-size: 15px;
  font-weight: 500;
  color: #1f2937;
}

.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.toolbar .el-button.active {
  background: #27ae60;
  border-color: #27ae60;
  color: #ffffff;
}

.image-compare {
  display: flex;
  gap: 16px;
  min-height: 400px;
}

.image-compare.grid {
  flex-direction: column;
}

.image-card {
  flex: 1;
  background: #f9fafb;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.compare-image {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
}

.image-label {
  position: absolute;
  bottom: 8px;
  left: 8px;
  background: rgba(0, 0, 0, 0.6);
  color: #ffffff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.right-panel {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 13px;
  color: #6b7280;
}

.info-value {
  font-size: 13px;
  color: #1f2937;
  font-weight: 500;
}

.result-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.empty-state {
  text-align: center;
  padding: 20px 0;
}

.empty-icon {
  font-size: 32px;
  color: #d1d5db;
  margin-bottom: 8px;
}

.empty-text {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 4px;
}

.empty-desc {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.detection-list {
  max-height: 200px;
  overflow-y: auto;
}

.detection-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}

.detection-item:last-child {
  border-bottom: none;
}

.item-name {
  font-size: 13px;
  color: #1f2937;
}

.item-confidence {
  font-size: 13px;
  color: #27ae60;
  font-weight: 500;
}

.diagnosis-content {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.5;
}

.diagnosis-content p {
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.btn-secondary {
  flex: 1;
}

.btn-primary {
  flex: 1;
}
</style>
