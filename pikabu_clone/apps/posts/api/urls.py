from django.urls import path
from .views import (
    PostCreateView,
    PostsListView,
    PostDetailView
)

app_name = 'post'
urlpatterns = [
    path('post/create/', PostCreateView.as_view()),
    path('all/', PostsListView.as_view()),
    path('post/detail/<int:pk>/', PostDetailView.as_view())
]
