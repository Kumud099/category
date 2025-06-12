from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'profile', views.UserProfileViewSet, basename='userprofile')

# Create nested router for comments under posts
posts_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', views.CommentViewSet, basename='post-comments')

urlpatterns = [
    # API overview and stats
    path('', views.api_overview, name='api-overview'),
    path('stats/', views.api_stats, name='api-stats'),
    
    # Include router URLs
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    
    # DRF browsable API authentication
    path('auth/', include('rest_framework.urls')),
]