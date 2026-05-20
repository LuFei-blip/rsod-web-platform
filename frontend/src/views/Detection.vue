<template>
  <div class="detection">
    <el-container>
      <el-header>
        <h1>遥感目标检测</h1>
        <el-button @click="$router.push('/')">返回首页</el-button>
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>上传图像</span>
                </div>
              </template>
              <el-upload
                class="upload-demo"
                drag
                :http-request="handleUpload"
                :show-file-list="false"
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  将图像拖到此处或<em>点击上传</em>
                </div>
              </el-upload>
              <div v-if="uploading" class="upload-progress">
                <el-progress :percentage="uploadProgress" />
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>检测结果</span>
                  <el-button 
                    v-if="uploadedImageUrl" 
                    type="primary" 
                    @click="handleDetect"
                    :loading="detecting"
                  >
                    开始检测
                  </el-button>
                </div>
              </template>
              <div v-if="uploadedImageUrl" class="result-image">
                <img :src="uploadedImageUrl" alt="上传图像" />
              </div>
              <el-empty v-else description="等待上传图像" />
              
              <div v-if="detectionResults.length > 0" class="detection-results">
                <h3>检测结果</h3>
                <el-table :data="detectionResults" style="width: 100%">
                  <el-table-column prop="class" label="目标类型" width="120" />
                  <el-table-column prop="confidence" label="置信度" width="100">
                    <template #default="scope">
                      {{ (scope.row.confidence * 100).toFixed(1) }}%
                    </template>
                  </el-table-column>
                  <el-table-column prop="bbox" label="边界框" />
                </el-table>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadImage, detectObjects } from '@/api'
import { ElMessage } from 'element-plus'

const uploadedImageUrl = ref('')
const detectionResults = ref<any[]>([])
const uploading = ref(false)
const uploadProgress = ref(0)
const detecting = ref(false)

const handleUpload = async (options: any) => {
  const file = options.file
  uploading.value = true
  uploadProgress.value = 0
  
  try {
    const response = await uploadImage(file)
    uploadedImageUrl.value = response.url
    uploadProgress.value = 100
    ElMessage.success('图像上传成功')
    
    // 清空之前的检测结果
    detectionResults.value = []
  } catch (error: any) {
    ElMessage.error(`上传失败: ${error.message || '未知错误'}`)
    console.error('Upload error:', error)
  } finally {
    uploading.value = false
  }
}

const handleDetect = async () => {
  if (!uploadedImageUrl.value) {
    ElMessage.warning('请先上传图像')
    return
  }
  
  detecting.value = true
  try {
    const response = await detectObjects(uploadedImageUrl.value)
    detectionResults.value = response.results || []
    ElMessage.success('检测完成')
  } catch (error: any) {
    ElMessage.error(`检测失败: ${error.message || '未知错误'}`)
    console.error('Detection error:', error)
  } finally {
    detecting.value = false
  }
}
</script>

<style scoped>
.detection {
  min-height: 100vh;
}

.el-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.el-header h1 {
  margin: 0;
  font-size: 24px;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}

.upload-demo {
  width: 100%;
}

.result-image {
  width: 100%;
  text-align: center;
}

.result-image img {
  max-width: 100%;
  height: auto;
}

.upload-progress {
  margin-top: 20px;
}

.detection-results {
  margin-top: 20px;
}

.detection-results h3 {
  margin-bottom: 10px;
  color: #409eff;
}

.model-tag {
  margin: 5px;
}
</style>
