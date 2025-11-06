import { InstagramPost } from '../types'
import { format } from 'date-fns'
import './InstagramPostCard.css'

interface InstagramPostCardProps {
  post: InstagramPost
  onDelete: (id: number) => void
}

function InstagramPostCard({ post, onDelete }: InstagramPostCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return '#fbbf24'
      case 'approved': return '#10b981'
      case 'posted': return '#8b5cf6'
      case 'failed': return '#ef4444'
      default: return '#aaa'
    }
  }

  return (
    <div className="instagram-card">
      <div className="instagram-image-container">
        {post.image_url ? (
          <img src={post.image_url} alt="Instagram post" className="instagram-image" />
        ) : (
          <div className="instagram-placeholder">
            <span>No image generated yet</span>
          </div>
        )}
        <span className="status-badge-overlay" style={{ backgroundColor: getStatusColor(post.status) }}>
          {post.status}
        </span>
      </div>

      <div className="instagram-content">
        <p className="instagram-caption">{post.caption}</p>

        <div className="instagram-meta">
          <span className="instagram-date">
            {format(new Date(post.created_at), 'MMM d, yyyy')}
          </span>
          {post.source_tweet_id && (
            <span className="source-badge">From Tweet #{post.source_tweet_id}</span>
          )}
        </div>

        <div className="instagram-actions">
          <button className="btn btn-sm btn-secondary">
            Edit Caption
          </button>
          <button className="btn btn-sm btn-primary">
            Download
          </button>
          <button className="btn btn-sm btn-danger" onClick={() => onDelete(post.id)}>
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}

export default InstagramPostCard
