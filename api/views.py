from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Follow, Group, User
from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
)
from .permissions import IsAuthorOrReadOnly


PERMISSION_CLASSES = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class CreateListGenericViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет класс для моделей Follow и Group, для урезания операций CRUD."""
    pass


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет класс для модели Post, выполняет любые операции CRUD."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = PERMISSION_CLASSES

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer, *args, **kwargs):
        params = {
            'author': self.request.user
        }
        serializer.save(**params)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет класс для модели Comment, выполняет любые операции CRUD."""
    serializer_class = CommentSerializer
    permission_classes = PERMISSION_CLASSES

    def perform_create(self, serializer):
        params = {
            'post_id': self.kwargs.get('post_id'),
            'author': self.request.user,
        }
        serializer.save(**params)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()


class FollowViewSet(CreateListGenericViewSet):
    """Вьюсет класс для модели Follow, выполняет GET И POST операции CRUD."""
    serializer_class = FollowSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filterset_fields = ['following', ]
    search_fields = ['user__username', 'following__username']

    def get_queryset(self):
        following = get_object_or_404(User, username=self.request.user)
        return Follow.objects.filter(following=following)

    def perform_create(self, serializer, *args, **kwargs):
        params = {
            'user': self.request.user
        }
        serializer.save(**params)


class GroupViewSet(CreateListGenericViewSet):
    """Вьюсет класс для модели Group, выполняет GET И POST операции CRUD."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = PERMISSION_CLASSES
