from django.urls import path
from .views import  browse_view,dashboard_view,profile_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('browse/', browse_view, name='browse_notes'),
    path('my-profile/',profile_view,name='profile'),
]