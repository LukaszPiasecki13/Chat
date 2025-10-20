# backend/chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('conversation/<int:user_id>/', views.ConversationListView.as_view(), name='conversation-list'),
]