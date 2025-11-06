import apiClient from './client'
import { Tweet, TweetUpdate } from '../types'

export const tweetsApi = {
  getAll: async (status?: string): Promise<Tweet[]> => {
    const params = status ? { status } : {}
    const response = await apiClient.get('/api/tweets/', { params })
    return response.data
  },

  getById: async (id: number): Promise<Tweet> => {
    const response = await apiClient.get(`/api/tweets/${id}`)
    return response.data
  },

  update: async (id: number, data: TweetUpdate): Promise<Tweet> => {
    const response = await apiClient.patch(`/api/tweets/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/tweets/${id}`)
  },

  generateTweets: async (count: number = 25): Promise<any> => {
    const response = await apiClient.post('/api/tweets/generate', { count })
    return response.data
  }
}
