from django.urls import path
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    register_view, login_view, logout_view, add_comment, delete_comment
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # CREATE post
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),  # DETAIL post
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('post/<slug:slug>/comment/', add_comment, name='add-comment'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete-comment'),
]
