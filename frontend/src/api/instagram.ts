import apiClient from './client'
import { InstagramPost, InstagramPostUpdate } from '../types'

export const instagramApi = {
  getAll: async (status?: string): Promise<InstagramPost[]> => {
    const params = status ? { status } : {}
    const response = await apiClient.get('/api/instagram/', { params })
    return response.data
  },

  getById: async (id: number): Promise<InstagramPost> => {
    const response = await apiClient.get(`/api/instagram/${id}`)
    return response.data
  },

  create: async (data: Partial<InstagramPost>): Promise<InstagramPost> => {
    const response = await apiClient.post('/api/instagram/', data)
    return response.data
  },

  update: async (id: number, data: InstagramPostUpdate): Promise<InstagramPost> => {
    const response = await apiClient.patch(`/api/instagram/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/instagram/${id}`)
  }
}
