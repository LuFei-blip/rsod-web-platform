<template>
  <div class="history-page">
    <div class="page-header">
      <div class="breadcrumb">
        <span>工作台</span>
        <span class="separator">›</span>
        <span class="active">历史记录</span>
      </div>
      <h1 class="page-title">检测历史记录</h1>
      <p class="page-subtitle">查看和管理所有检测任务的历史记录</p>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        style="width: 240px"
      />
      <el-select v-model="modelFilter" placeholder="选择模型" style="width: 160px; margin-left: 12px">
        <el-option label="全部模型" value="" />
        <el-option label="pest-v1" value="pest-v1" />
        <el-option label="pest-v2" value="pest-v2" />
      </el-select>
      <el-button type="primary" style="margin-left: 12px" @click="fetchHistory">
        <el-icon><Search /></el-icon>
        查询
      </el-button>
    </div>

    <!-- 历史记录表格 -->
    <div class="table-container">
      <el-table :data="historyList" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="任务ID" width="200" />
        <el-table-column label="原始图片" width="120">
          <template #default="{ row }">
            <el-image
              :src="row.image_url"
              style="width: 80px; height: 60px"
              fit="cover"
              :preview-src-list="[row.image_url]"
            />
          </template>
        </el-table-column>
        <el-table-column label="结果图片" width="120">
          <template #default="{ row }">
            <el-image
              :src="row.result_image_url"
              style="width: 80px; height: 60px"
              fit="cover"
              :preview-src-list="[row.result_image_url]"
            />
          </template>
        </el-table-column>
        <el-table-column prop="total_objects" label="检测目标数" width="120" />
        <el-table-column prop="model_name" label="检测模型" width="120" />
        <el-table-column prop="created_at" label="检测时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="150">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="viewDetail(row)">查看详情</el-button>
            <el-button size="small" type="danger" @click="deleteRecord(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="fetchHistory"
          @current-change="fetchHistory"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Search } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { getDetectionHistory, type HistoryItem } from "../api/detection";

const historyList = ref<HistoryItem[]>([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);
const dateRange = ref<[Date, Date] | null>(null);
const modelFilter = ref("");

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleString("zh-CN");
};

const fetchHistory = async () => {
  loading.value = true;
  try {
    // 模拟数据
    historyList.value = [
      {
        id: "det-001",
        image_url: "",
        result_image_url: "",
        total_objects: 5,
        created_at: new Date().toISOString(),
        model_name: "pest-v1",
      },
      {
        id: "det-002",
        image_url: "",
        result_image_url: "",
        total_objects: 3,
        created_at: new Date(Date.now() - 86400000).toISOString(),
        model_name: "pest-v2",
      },
    ];
    total.value = 2;
    ElMessage.success("加载成功");
  } catch (error) {
    ElMessage.error("加载失败");
  } finally {
    loading.value = false;
  }
};

const viewDetail = (row: HistoryItem) => {
  ElMessage.info(`查看记录 ${row.id} 详情`);
};

const deleteRecord = async (row: HistoryItem) => {
  try {
    await ElMessageBox.confirm("确定要删除这条记录吗？", "确认删除", {
      type: "warning",
    });
    ElMessage.success("删除成功");
    fetchHistory();
  } catch {
    // 用户取消
  }
};

onMounted(() => {
  fetchHistory();
});
</script>

<style scoped>
.history-page {
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

.filter-bar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  background: #ffffff;
  padding: 16px;
  border-radius: 8px;
}

.table-container {
  background: #ffffff;
  border-radius: 8px;
  padding: 16px;
}

.pagination {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
