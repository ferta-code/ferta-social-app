import { useState } from 'react'
import { Tweet, TweetUpdate } from '../types'
import { formatInTimeZone } from 'date-fns-tz'
import './TweetCard.css'

// Central Time timezone
const CENTRAL_TZ = 'America/Chicago'

// Helper to format dates in Central Time
const formatCT = (dateString: string, formatStr: string) => {
  return formatInTimeZone(new Date(dateString), CENTRAL_TZ, formatStr)
}

interface TweetCardProps {
  tweet: Tweet
  onUpdate: (id: number, data: TweetUpdate) => void
  onDelete: (id: number) => void
}

function TweetCard({ tweet, onUpdate, onDelete }: TweetCardProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editedContent, setEditedContent] = useState(tweet.content)
  const [showScheduler, setShowScheduler] = useState(false)
  const [scheduledDate, setScheduledDate] = useState('')
  const [scheduledTime, setScheduledTime] = useState('')

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
    if (!scheduledDate || !scheduledTime) {
      alert('Please select both date and time')
      return
    }

    const scheduledDateTime = new Date(`${scheduledDate}T${scheduledTime}`)

    if (scheduledDateTime < new Date()) {
      alert('Scheduled time must be in the future')
      return
    }

    onUpdate(tweet.id, {
      status: 'scheduled',
      scheduled_time: scheduledDateTime.toISOString()
    })
    setShowScheduler(false)
    setScheduledDate('')
    setScheduledTime('')
  }

  const handleQuickSchedule = (hoursFromNow: number) => {
    const scheduledTime = new Date()
    scheduledTime.setHours(scheduledTime.getHours() + hoursFromNow)
    onUpdate(tweet.id, {
      status: 'scheduled',
      scheduled_time: scheduledTime.toISOString()
    })
  }

  const handleUnschedule = () => {
    onUpdate(tweet.id, { status: 'approved', scheduled_time: undefined })
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
          Created: {formatCT(tweet.created_at, 'MMM d, yyyy h:mm a')} CT
        </span>
        {tweet.edited && <span className="edited-badge">Edited</span>}
      </div>

      {tweet.scheduled_time && (
        <div className="scheduled-time">
          <strong>⏰ Scheduled for:</strong> {formatCT(tweet.scheduled_time, 'MMM d, yyyy h:mm a')} CT
        </div>
      )}

      {showScheduler && (
        <div className="scheduler-modal">
          <h4>Schedule Tweet</h4>
          <div className="quick-schedule">
            <p>Quick schedule:</p>
            <button className="btn btn-sm" onClick={() => handleQuickSchedule(1)}>+1 hour</button>
            <button className="btn btn-sm" onClick={() => handleQuickSchedule(4)}>+4 hours</button>
            <button className="btn btn-sm" onClick={() => handleQuickSchedule(24)}>+1 day</button>
          </div>
          <div className="custom-schedule">
            <p>Or choose custom time:</p>
            <input
              type="date"
              value={scheduledDate}
              onChange={(e) => setScheduledDate(e.target.value)}
              min={new Date().toISOString().split('T')[0]}
            />
            <input
              type="time"
              value={scheduledTime}
              onChange={(e) => setScheduledTime(e.target.value)}
            />
          </div>
          <div className="scheduler-actions">
            <button className="btn btn-sm btn-primary" onClick={handleSchedule}>
              Confirm
            </button>
            <button className="btn btn-sm btn-secondary" onClick={() => setShowScheduler(false)}>
              Cancel
            </button>
          </div>
        </div>
      )}

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
              <button className="btn btn-sm btn-primary" onClick={() => setShowScheduler(true)}>
                Schedule
              </button>
            )}
            {tweet.status === 'scheduled' && (
              <button className="btn btn-sm btn-warning" onClick={handleUnschedule}>
                Unschedule
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
