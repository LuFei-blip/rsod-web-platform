<template>
  <div class="profile-page">
    <div class="page-header">
      <div class="breadcrumb">
        <span>工作台</span>
        <span class="separator">›</span>
        <span class="active">个人中心</span>
      </div>
      <h1 class="page-title">个人中心</h1>
      <p class="page-subtitle">管理您的个人信息和账户设置</p>
    </div>

    <div class="profile-container">
      <!-- 个人信息卡片 -->
      <div class="profile-card">
        <div class="avatar-section">
          <el-avatar :size="80" style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)">
            <span style="font-size: 32px">{{ userInfo.username.charAt(0).toUpperCase() }}</span>
          </el-avatar>
          <h2 class="username">{{ userInfo.username }}</h2>
          <p class="user-email">{{ userInfo.email }}</p>
        </div>
      </div>

      <!-- 信息编辑表单 -->
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span>基本信息</span>
            <el-button type="primary" size="small" @click="handleSave" :loading="saving">
              保存修改
            </el-button>
          </div>
        </template>
        <el-form :model="userInfo" label-width="100px" style="max-width: 500px">
          <el-form-item label="用户名">
            <el-input v-model="userInfo.username" disabled />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="userInfo.email" placeholder="请输入邮箱" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="userInfo.phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="注册时间">
            <el-input :model-value="userInfo.registerDate" disabled />
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 修改密码 -->
      <el-card class="password-card">
        <template #header>
          <span>修改密码</span>
        </template>
        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-width="100px"
          style="max-width: 500px"
        >
          <el-form-item label="当前密码" prop="currentPassword">
            <el-input v-model="passwordForm.currentPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="passwordForm.newPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleChangePassword" :loading="changingPassword">
              修改密码
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 使用统计 -->
      <el-card class="stats-card">
        <template #header>
          <span>使用统计</span>
        </template>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.totalDetections }}</div>
              <div class="stat-label">总检测次数</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.totalTargets }}</div>
              <div class="stat-label">检测目标总数</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.daysUsed }}</div>
              <div class="stat-label">使用天数</div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";

const userInfo = reactive({
  username: "用户",
  email: "",
  phone: "",
  registerDate: "2026-05-19",
});

const saving = ref(false);

const handleSave = async () => {
  saving.value = true;
  setTimeout(() => {
    saving.value = false;
    ElMessage.success("保存成功");
  }, 500);
};

const passwordForm = reactive({
  currentPassword: "",
  newPassword: "",
  confirmPassword: "",
});

const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error("两次输入的密码不一致"));
  } else {
    callback();
  }
};

const passwordRules = reactive<FormRules>({
  currentPassword: [{ required: true, message: "请输入当前密码", trigger: "blur" }],
  newPassword: [
    { required: true, message: "请输入新密码", trigger: "blur" },
    { min: 6, max: 30, message: "密码长度在6到30个字符", trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: "请确认密码", trigger: "blur" },
    { validator: validateConfirmPassword, trigger: "blur" },
  ],
});

const passwordFormRef = ref<FormInstance>();
const changingPassword = ref(false);

const handleChangePassword = () => {
  if (!passwordFormRef.value) return;
  passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      changingPassword.value = true;
      setTimeout(() => {
        changingPassword.value = false;
        ElMessage.success("密码修改成功");
        passwordForm.currentPassword = "";
        passwordForm.newPassword = "";
        passwordForm.confirmPassword = "";
      }, 500);
    }
  });
};

const stats = reactive({
  totalDetections: 0,
  totalTargets: 0,
  daysUsed: 1,
});

onMounted(() => {
  const username = localStorage.getItem("username") || "用户";
  userInfo.username = username;
});
</script>

<style scoped>
.profile-page {
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

.profile-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.username {
  font-size: 22px;
  font-weight: 600;
  color: #1f2937;
  margin: 16px 0 8px;
}

.user-email {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.info-card,
.password-card,
.stats-card {
  background: #ffffff;
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-item {
  text-align: center;
  padding: 20px 0;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #27ae60;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}
</style>
