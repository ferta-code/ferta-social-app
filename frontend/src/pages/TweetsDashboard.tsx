import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { tweetsApi } from '../api/tweets'
import { Tweet, TweetUpdate } from '../types'
import TweetCard from '../components/TweetCard'
import './TweetsDashboard.css'

function TweetsDashboard() {
  const queryClient = useQueryClient()
  const [filter, setFilter] = useState<string>('all')

  const { data: tweets, isLoading, error } = useQuery({
    queryKey: ['tweets', filter],
    queryFn: () => tweetsApi.getAll(filter === 'all' ? undefined : filter)
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: TweetUpdate }) =>
      tweetsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tweets'] })
    }
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => tweetsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tweets'] })
    }
  })

  const generateMutation = useMutation({
    mutationFn: () => tweetsApi.generateTweets(25),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tweets'] })
    }
  })

  const handleUpdateTweet = (id: number, data: TweetUpdate) => {
    updateMutation.mutate({ id, data })
  }

  const handleDeleteTweet = (id: number) => {
    if (confirm('Are you sure you want to delete this tweet?')) {
      deleteMutation.mutate(id)
    }
  }

  const handleGenerateTweets = () => {
    generateMutation.mutate()
  }

  if (isLoading) return <div className="loading">Loading tweets...</div>
  if (error) return <div className="error">Error loading tweets: {(error as Error).message}</div>

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Tweet Ideas</h2>
        <div className="header-actions">
          <select
            className="filter-select"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="all">All</option>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="scheduled">Scheduled</option>
            <option value="posted">Posted</option>
          </select>
          <button
            className="btn btn-primary"
            onClick={handleGenerateTweets}
            disabled={generateMutation.isPending}
          >
            {generateMutation.isPending ? 'Generating...' : 'Generate New Tweets'}
          </button>
        </div>
      </div>

      <div className="tweets-grid">
        {tweets && tweets.length > 0 ? (
          tweets.map((tweet: Tweet) => (
            <TweetCard
              key={tweet.id}
              tweet={tweet}
              onUpdate={handleUpdateTweet}
              onDelete={handleDeleteTweet}
            />
          ))
        ) : (
          <div className="empty-state">
            <p>No tweets found. Generate some new ideas!</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default TweetsDashboard
