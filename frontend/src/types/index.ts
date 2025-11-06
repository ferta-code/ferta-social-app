export interface Tweet {
  id: number
  content: string
  ai_source: string
  status: 'pending' | 'approved' | 'scheduled' | 'posted' | 'failed'
  scheduled_time: string | null
  posted_time: string | null
  created_at: string
  edited: boolean
  twitter_id: string | null
}

export interface InstagramPost {
  id: number
  source_tweet_id: number | null
  caption: string
  image_url: string
  status: 'pending' | 'approved' | 'posted' | 'failed'
  posted_time: string | null
  created_at: string
  instagram_id: string | null
}

export interface TweetUpdate {
  content?: string
  status?: string
  scheduled_time?: string
}

export interface InstagramPostUpdate {
  caption?: string
  status?: string
}
