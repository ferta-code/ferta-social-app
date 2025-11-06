import { useState } from 'react'
import { Tweet, TweetUpdate } from '../types'
import { format } from 'date-fns'
import './TweetCard.css'

interface TweetCardProps {
  tweet: Tweet
  onUpdate: (id: number, data: TweetUpdate) => void
  onDelete: (id: number) => void
}

function TweetCard({ tweet, onUpdate, onDelete }: TweetCardProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editedContent, setEditedContent] = useState(tweet.content)

  const handleSave = () => {
    if (editedContent !== tweet.content) {
      onUpdate(tweet.id, { content: editedContent })
    }
    setIsEditing(false)
  }

  const handleApprove = () => {
    onUpdate(tweet.id, { status: 'approved' })
  }

  const handleSchedule = () => {
    // In a real app, this would open a datetime picker
    const scheduledTime = new Date()
    scheduledTime.setHours(scheduledTime.getHours() + 1)
    onUpdate(tweet.id, {
      status: 'scheduled',
      scheduled_time: scheduledTime.toISOString()
    })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return '#fbbf24'
      case 'approved': return '#10b981'
      case 'scheduled': return '#3b82f6'
      case 'posted': return '#8b5cf6'
      case 'failed': return '#ef4444'
      default: return '#aaa'
    }
  }

  return (
    <div className="tweet-card">
      <div className="tweet-header">
        <span className="ai-badge" style={{
          backgroundColor: tweet.ai_source === 'claude' ? '#c17b5f' : '#10a37f'
        }}>
          {tweet.ai_source === 'claude' ? 'Claude' : 'ChatGPT'}
        </span>
        <span className="status-badge" style={{ backgroundColor: getStatusColor(tweet.status) }}>
          {tweet.status}
        </span>
      </div>

      <div className="tweet-content">
        {isEditing ? (
          <textarea
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            className="tweet-textarea"
            rows={4}
          />
        ) : (
          <p className="tweet-text">{tweet.content}</p>
        )}
      </div>

      <div className="tweet-meta">
        <span className="tweet-date">
          {format(new Date(tweet.created_at), 'MMM d, yyyy h:mm a')}
        </span>
        {tweet.edited && <span className="edited-badge">Edited</span>}
      </div>

      <div className="tweet-actions">
        {isEditing ? (
          <>
            <button className="btn btn-sm btn-success" onClick={handleSave}>
              Save
            </button>
            <button className="btn btn-sm btn-secondary" onClick={() => {
              setEditedContent(tweet.content)
              setIsEditing(false)
            }}>
              Cancel
            </button>
          </>
        ) : (
          <>
            <button className="btn btn-sm btn-secondary" onClick={() => setIsEditing(true)}>
              Edit
            </button>
            {tweet.status === 'pending' && (
              <button className="btn btn-sm btn-success" onClick={handleApprove}>
                Approve
              </button>
            )}
            {tweet.status === 'approved' && (
              <button className="btn btn-sm btn-primary" onClick={handleSchedule}>
                Schedule
              </button>
            )}
            <button className="btn btn-sm btn-danger" onClick={() => onDelete(tweet.id)}>
              Delete
            </button>
          </>
        )}
      </div>
    </div>
  )
}

export default TweetCard
