from django.urls import path
from .views import  browse_view,dashboard_view,profile_view,edit_profile_view,leaderboard_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('browse/', browse_view, name='browse_notes'),
    path('my-profile/',profile_view,name='profile'),
    path('edit-profile/',edit_profile_view,name='edit_profile'),
    path('leaderboard/',leaderboard_view,name='leaderboard'),
]