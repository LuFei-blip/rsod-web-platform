import request from '../utils/request'

export interface DetectionBox {
  x1: number
  y1: number
  x2: number
  y2: number
  confidence: number
  class_id: number
  class_name: string
}

export interface DetectionResult {
  detection_id: string
  image_url: string
  result_image_url: string
  boxes: DetectionBox[]
  total_objects: number
  detection_time: number
  model_name: string
  created_at: string
}

export interface SingleDetectionResponse {
  success: boolean
  message: string
  data?: DetectionResult
}

export interface HistoryItem {
  id: string
  image_url: string
  result_image_url: string
  total_objects: number
  created_at: string
  model_name: string
}

export interface HistoryResponse {
  success: boolean
  message: string
  data: HistoryItem[]
  total: number
}

export interface TargetItem {
  id: number
  name: string
  chinese_name: string
  description?: string
}

export interface TargetListResponse {
  success: boolean
  message: string
  data: TargetItem[]
}

// 单图检测接口
export const detectSingleImage = (data: FormData): Promise<SingleDetectionResponse> => {
  return request({
    url: '/detection/single',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取检测历史
export const getDetectionHistory = (params?: { page?: number; limit?: number }): Promise<HistoryResponse> => {
  return request({
    url: '/detection/history',
    method: 'get',
    params
  })
}

// 获取检测详情
export const getDetectionDetail = (id: string): Promise<SingleDetectionResponse> => {
  return request({
    url: `/detection/detail/${id}`,
    method: 'get'
  })
}

// 获取目标库列表
export const getTargetList = (): Promise<TargetListResponse> => {
  return request({
    url: '/detection/targets/list',
    method: 'get'
  })
}
