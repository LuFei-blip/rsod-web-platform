<template>
  <div class="home">
    <el-container>
      <el-header>
        <h1>遥感目标检测平台</h1>
        <el-tag v-if="apiStatus" type="success" size="small">
          API已连接
        </el-tag>
        <el-tag v-else type="danger" size="small">
          API未连接
        </el-tag>
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>目标检测</span>
                </div>
              </template>
              <p>上传遥感图像进行目标检测</p>
              <el-button type="primary" @click="$router.push('/detect')">
                开始检测
              </el-button>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>可用模型</span>
                </div>
              </template>
              <div v-if="models.length > 0">
                <el-tag 
                  v-for="model in models" 
                  :key="model.name" 
                  class="model-tag"
                  type="info"
                >
                  {{ model.name }} - {{ model.type }}
                </el-tag>
              </div>
              <p v-else>加载中...</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>系统状态</span>
                </div>
              </template>
              <p>后端服务: {{ apiStatus ? '运行中' : '未连接' }}</p>
              <p>模型服务: 待实现</p>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { healthCheck, getModels } from '@/api'

const apiStatus = ref(false)
const models = ref<any[]>([])

onMounted(async () => {
  try {
    // 检查API健康状态
    await healthCheck()
    apiStatus.value = true
    
    // 获取模型列表
    const response = await getModels()
    models.value = response.models || []
  } catch (error) {
    console.error('API连接失败:', error)
    apiStatus.value = false
  }
})
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.el-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
}

.el-header h1 {
  margin: 0;
  font-size: 24px;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}

.el-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
