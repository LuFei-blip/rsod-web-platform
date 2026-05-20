import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    const message = error.response?.data?.detail || error.message || '未知错误'
    return Promise.reject(new Error(message))
  }
)

// API方法
export const uploadImage = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const detectObjects = (imageUrl: string) => {
  return api.post('/detect', null, {
    params: { image_url: imageUrl }
  })
}

export const getModels = () => {
  return api.get('/models')
}

export const healthCheck = () => {
  return api.get('/health')
}

export default api
