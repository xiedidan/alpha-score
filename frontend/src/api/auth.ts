/**
 * 认证相关API
 */
import { api } from './request'

// 登录请求参数
export interface LoginRequest {
  username: string
  password: string
}

// 登录响应数据
export interface LoginResponse {
  code: number
  message: string
  data: {
    access_token: string
    token_type: string
    expires_in: number
  }
}

// 用户信息响应
export interface UserInfoResponse {
  code: number
  message: string
  data: {
    id: number
    username: string
    role: string
    is_active: boolean
    last_login: string | null
    created_at: string
    updated_at: string
  }
}

/**
 * 用户登录
 */
export function login(data: LoginRequest): Promise<LoginResponse> {
  return api.post('/auth/login', data)
}

/**
 * 用户登出
 */
export function logout(): Promise<any> {
  return api.post('/auth/logout')
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser(): Promise<UserInfoResponse> {
  return api.get('/auth/me')
}
