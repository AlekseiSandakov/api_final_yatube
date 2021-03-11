from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator

User = get_user_model()


class Post(models.Model):
    """Модель приложения POSTS, отвечает за создание постов."""
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    group = models.ForeignKey('Group', blank=True, null=True,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              verbose_name='community', )

    def __str__(self):
        self.text = Truncator(self.text).words(10)
        return self.text


class Comment(models.Model):
    """Модель приложения POSTS, отвечает за создание комментариев к постам."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    """Модель приложения POSTS, отвечает за создание подписок к постам."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower',
        help_text='Пользователь',
        null=True,
    )
    following = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
        help_text='Автор поста',
        null=True,
    )

    def __str__(self):
        return f'{self.user} {self.following}'


class Group(models.Model):
    """Модель приложения POSTS, отвечает за создание групп из постов."""
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        help_text='Напишите заголовок',
    )

    def __str__(self):
        return self.title
