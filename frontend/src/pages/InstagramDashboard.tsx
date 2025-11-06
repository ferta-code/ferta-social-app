import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { instagramApi } from '../api/instagram'
import { InstagramPost } from '../types'
import InstagramPostCard from '../components/InstagramPostCard'
import './InstagramDashboard.css'

function InstagramDashboard() {
  const queryClient = useQueryClient()

  const { data: posts, isLoading, error } = useQuery({
    queryKey: ['instagram'],
    queryFn: () => instagramApi.getAll()
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => instagramApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['instagram'] })
    }
  })

  const handleDelete = (id: number) => {
    if (confirm('Are you sure you want to delete this post?')) {
      deleteMutation.mutate(id)
    }
  }

  if (isLoading) return <div className="loading">Loading Instagram posts...</div>
  if (error) return <div className="error">Error loading posts: {(error as Error).message}</div>

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Instagram Posts</h2>
        <p className="subtitle">Convert approved tweets into Instagram posts</p>
      </div>

      <div className="instagram-grid">
        {posts && posts.length > 0 ? (
          posts.map((post: InstagramPost) => (
            <InstagramPostCard
              key={post.id}
              post={post}
              onDelete={handleDelete}
            />
          ))
        ) : (
          <div className="empty-state">
            <p>No Instagram posts yet. Select a tweet to convert!</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default InstagramDashboard
