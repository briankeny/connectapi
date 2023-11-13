from django.urls import path
from .views import PostList,PostDetail

app_name = 'posts'
urlpatterns = [
    path('posts/',PostList.as_view(), name='create-post'),
    path('post/<int:pk>/', PostDetail.as_view(), name='edit-post'),
]








