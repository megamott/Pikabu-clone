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
    path('post/create/', PostCreateView.as_view()),
    path('all/', PostsListView.as_view()),
    path('post/detail/<int:pk>/', PostDetailView.as_view()),
    path('comments/post/<int:pk>/comments/', PostCommentListView.as_view()),
    path('comments/post/<int:pk>/comment/create/', CommentCreateView.as_view()),
    path('comments/post/<int:pk1>/comment/detail/<int:pk>/', CommentDetailView.as_view())
]
