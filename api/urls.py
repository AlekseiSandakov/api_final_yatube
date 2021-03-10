from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet


router_V1 = DefaultRouter()
router_V1.register(
    'posts',
    PostViewSet,
    basename='posts',
)
router_V1.register(
    'posts/<int:post_id>',
    PostViewSet,
    basename='posts',
)
router_V1.register(
    'group',
    GroupViewSet,
    basename='group',
)
router_V1.register(
    'follow',
    FollowViewSet,
    basename='follow',
)
router_V1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router_V1.urls)),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
