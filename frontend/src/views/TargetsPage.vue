<template>
  <div class="targets-page">
    <div class="page-header">
      <div class="breadcrumb">
        <span>工作台</span>
        <span class="separator">›</span>
        <span class="active">目标库</span>
      </div>
      <h1 class="page-title">目标类型库</h1>
      <p class="page-subtitle">查看支持检测的所有目标类型及其说明</p>
    </div>

    <div class="targets-grid" v-loading="loading">
      <div
        v-for="target in targetList"
        :key="target.id"
        class="target-card"
      >
        <div class="target-icon">
          <el-icon :size="40" color="#27ae60"><View /></el-icon>
        </div>
        <div class="target-info">
          <h3 class="target-name">{{ target.chinese_name }}</h3>
          <p class="target-name-en">{{ target.name }}</p>
          <p class="target-desc">{{ target.description || "暂无描述" }}</p>
        </div>
        <div class="target-actions">
          <el-button size="small" type="primary" @click="viewTarget(target)">
            查看示例
          </el-button>
        </div>
      </div>
    </div>

    <!-- 示例图片弹窗 -->
    <el-dialog v-model="dialogVisible" :title="`${currentTarget?.chinese_name} - 示例图片`" width="800px">
      <div class="example-images">
        <el-empty description="示例图片加载中..." />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { View } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { getTargetList, type TargetItem } from "../api/detection";

const targetList = ref<TargetItem[]>([]);
const loading = ref(false);
const dialogVisible = ref(false);
const currentTarget = ref<TargetItem | null>(null);

const viewTarget = (target: TargetItem) => {
  currentTarget.value = target;
  dialogVisible.value = true;
};

const fetchTargets = async () => {
  loading.value = true;
  try {
    const response = await getTargetList();
    if (response.success) {
      targetList.value = response.data;
    }
  } catch (error) {
    // 使用模拟数据
    targetList.value = [
      { id: 0, name: "airplane", chinese_name: "飞机", description: "固定翼飞机、直升机等" },
      { id: 1, name: "oil_tank", chinese_name: "油罐", description: "储油罐、化工罐等" },
      { id: 2, name: "playground", chinese_name: "操场", description: "运动场、操场等" },
      { id: 3, name: "building", chinese_name: "建筑物", description: "各类建筑物" },
      { id: 4, name: "ship", chinese_name: "船舶", description: "各类船舶" },
      { id: 5, name: "pest", chinese_name: "农业虫害", description: "农作物病虫害" },
    ];
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchTargets();
});
</script>

<style scoped>
.targets-page {
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

.targets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.target-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.target-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.target-icon {
  width: 64px;
  height: 64px;
  background: #f0fdf4;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.target-info {
  flex: 1;
}

.target-name {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px;
}

.target-name-en {
  font-size: 13px;
  color: #6b7280;
  margin: 0 0 8px;
}

.target-desc {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
}

.target-actions {
  margin-top: 16px;
}

.example-images {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
