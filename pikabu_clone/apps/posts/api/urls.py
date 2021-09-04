from django.urls import path

from .views import (
    PostCreateView,
    PostsListView,
    PostDetailView,
    PostCommentListView,
    CommentCreateView,
    CommentDetailView
)

app_name = 'post'
urlpatterns = [
    path('post/create/', PostCreateView.as_view(), name='create-post'),
    path('all/', PostsListView.as_view(), name='list-posts'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/post/<int:pk>/comments/', PostCommentListView.as_view(), name='post-comments'),
    path('comments/post/<int:pk>/comment/create/', CommentCreateView.as_view(), name='create-comment'),
    path('comments/post/<int:pk1>/comment/detail/<int:pk>/', CommentDetailView.as_view(), name='comment-detail')
]
