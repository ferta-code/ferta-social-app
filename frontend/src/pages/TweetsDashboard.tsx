import { useState, useMemo } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { tweetsApi } from '../api/tweets'
import { Tweet, TweetUpdate } from '../types'
import TweetCard from '../components/TweetCard'
import './TweetsDashboard.css'

function TweetsDashboard() {
  const queryClient = useQueryClient()
  const [viewMode, setViewMode] = useState<'kanban' | 'list'>('kanban')

  const { data: tweets, isLoading, error } = useQuery({
    queryKey: ['tweets'],
    queryFn: () => tweetsApi.getAll()
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

  // Group tweets by status for Kanban view
  const tweetsByStatus = useMemo(() => {
    if (!tweets) return { pending: [], approved: [], scheduled: [], posted: [] }

    return {
      pending: tweets.filter((t: Tweet) => t.status === 'pending'),
      approved: tweets.filter((t: Tweet) => t.status === 'approved'),
      scheduled: tweets.filter((t: Tweet) => t.status === 'scheduled').sort((a: Tweet, b: Tweet) => {
        if (!a.scheduled_time || !b.scheduled_time) return 0
        return new Date(a.scheduled_time).getTime() - new Date(b.scheduled_time).getTime()
      }),
      posted: tweets.filter((t: Tweet) => t.status === 'posted')
    }
  }, [tweets])

  if (isLoading) return <div className="loading">Loading tweets...</div>
  if (error) return <div className="error">Error loading tweets: {(error as Error).message}</div>

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Tweet Ideas</h2>
        <div className="header-actions">
          <div className="view-toggle">
            <button
              className={`btn btn-sm ${viewMode === 'kanban' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setViewMode('kanban')}
            >
              Kanban
            </button>
            <button
              className={`btn btn-sm ${viewMode === 'list' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setViewMode('list')}
            >
              List
            </button>
          </div>
          <button
            className="btn btn-primary"
            onClick={handleGenerateTweets}
            disabled={generateMutation.isPending}
          >
            {generateMutation.isPending ? 'Generating...' : 'Generate New Tweets'}
          </button>
        </div>
      </div>

      {viewMode === 'kanban' ? (
        <div className="kanban-board">
          <div className="kanban-column">
            <div className="column-header">
              <h3>Pending Review</h3>
              <span className="tweet-count">{tweetsByStatus.pending.length}</span>
            </div>
            <div className="column-content">
              {tweetsByStatus.pending.map((tweet: Tweet) => (
                <TweetCard
                  key={tweet.id}
                  tweet={tweet}
                  onUpdate={handleUpdateTweet}
                  onDelete={handleDeleteTweet}
                />
              ))}
              {tweetsByStatus.pending.length === 0 && (
                <div className="empty-column">No pending tweets</div>
              )}
            </div>
          </div>

          <div className="kanban-column">
            <div className="column-header">
              <h3>Approved</h3>
              <span className="tweet-count">{tweetsByStatus.approved.length}</span>
            </div>
            <div className="column-content">
              {tweetsByStatus.approved.map((tweet: Tweet) => (
                <TweetCard
                  key={tweet.id}
                  tweet={tweet}
                  onUpdate={handleUpdateTweet}
                  onDelete={handleDeleteTweet}
                />
              ))}
              {tweetsByStatus.approved.length === 0 && (
                <div className="empty-column">No approved tweets</div>
              )}
            </div>
          </div>

          <div className="kanban-column">
            <div className="column-header">
              <h3>Scheduled</h3>
              <span className="tweet-count">{tweetsByStatus.scheduled.length}</span>
            </div>
            <div className="column-content">
              {tweetsByStatus.scheduled.map((tweet: Tweet) => (
                <TweetCard
                  key={tweet.id}
                  tweet={tweet}
                  onUpdate={handleUpdateTweet}
                  onDelete={handleDeleteTweet}
                />
              ))}
              {tweetsByStatus.scheduled.length === 0 && (
                <div className="empty-column">No scheduled tweets</div>
              )}
            </div>
          </div>

          <div className="kanban-column">
            <div className="column-header">
              <h3>Posted</h3>
              <span className="tweet-count">{tweetsByStatus.posted.length}</span>
            </div>
            <div className="column-content">
              {tweetsByStatus.posted.map((tweet: Tweet) => (
                <TweetCard
                  key={tweet.id}
                  tweet={tweet}
                  onUpdate={handleUpdateTweet}
                  onDelete={handleDeleteTweet}
                />
              ))}
              {tweetsByStatus.posted.length === 0 && (
                <div className="empty-column">No posted tweets</div>
              )}
            </div>
          </div>
        </div>
      ) : (
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
      )}
    </div>
  )
}

export default TweetsDashboard
