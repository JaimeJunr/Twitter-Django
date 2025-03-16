from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django import forms

def user_directory_path(instance, filename):
    """Gera o caminho de upload para imagens de usuário."""
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.id, filename)

class User(AbstractUser):
    """Modelo de usuário personalizado, estendendo o AbstractUser do Django."""

    email = models.EmailField(unique=True, null=False, blank=False)
    image = models.ImageField(
        upload_to=user_directory_path,
        max_length=1000,
        null=True,
        blank=True,
        default="default.png",
    )
    cover_image = models.ImageField(
        upload_to=user_directory_path,
        max_length=1000,
        null=True,
        blank=True,
        default="cover_default.jpg",
    )
    bio = models.TextField(max_length=160, blank=True)  # Campo de bio para usuários
    website = models.URLField(
        max_length=200, blank=True
    )  # Campo para URL do site do usuário
    is_active = models.BooleanField(default=True)  # Indica se o usuário está ativo

    follower_count = models.PositiveIntegerField(default=0, editable=False)
    following_count = models.PositiveIntegerField(default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_follower_count(self):
        """Atualiza o contador de seguidores."""
        self.follower_count = self.followers.count()


    def update_following_count(self):
        """Atualiza o contador de seguidos."""
        self.following_count = self.followings.count()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        self.update_follower_count()
        self.update_following_count()

        if not is_new:
            super().save(update_fields=['follower_count', 'following_count'])
            

    def __str__(self):
        return f"{self.username} ({self.email})"

class Tweet(models.Model):
    """Modelo para representar um tweet."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField(max_length=280, blank=True)  # Conteúdo do tweet ou retweet comentado
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_retweet = models.BooleanField(default=False)  # Indica se é um retweet
    original_tweet = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="retweets_original",
        on_delete=models.CASCADE,
    )  # Para retweets Para referência ao tweet original, caso seja um retweet
    users_liked = models.ManyToManyField(User, related_name="liked_tweets", blank=True)

    class Meta:
        verbose_name = "Tweet"
        verbose_name_plural = "Tweets"
        ordering = ["-created_at"]

    def __str__(self):
        if self.is_retweet and not self.content:
            return f"Retweet de {self.original_tweet.user.username}"
        elif self.is_retweet and self.content:
            return f"{self.user.username} comentou no retweet: {self.content[:50]}..."
        else:
            return self.content[:50] + "..." if len(self.content) > 50 else self.content

    def clean(self):
        """Validações personalizadas."""
        if self.is_retweet and not self.original_tweet:
            raise ValidationError("Um retweet deve ter um tweet original.")

        if self.is_retweet:
            if len(self.content) > 280:
                raise ValidationError("O comentário do retweet não pode exceder 280 caracteres.")

    def like_count(self):
        return self.tweet_likes.count()

    def comment_count(self):
        return self.comments.count()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Like(models.Model):
    """Modelo para representar um like em um tweet."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="tweet_likes") 
    created_at = models.DateTimeField(auto_now_add=True)  # Data do "like"

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ("user", "tweet")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} liked {self.tweet.content[:50]}..."


class Comment(models.Model):
    """Modelo para representar um comentário em um tweet."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=280)  # Limitar o tamanho do comentário
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.SET_NULL
    )  # Para comentários em resposta

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} commented: {self.content[:50]}..."
            if len(self.content) > 50
            else self.content
        )


class Follow(models.Model):
    """Modelo para representar o relacionamento de seguir entre usuários."""

    follower = models.ForeignKey(
        User, related_name="followings", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp para seguimento

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        unique_together = ("follower", "following")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower.username} followed {self.following.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Atualiza contagens de seguidores/seguindo
        self.follower.update_following_count()
        self.following.update_follower_count()

    def delete(self, *args, **kwargs):
        # Antes de deletar, atualizar contagens de seguidores
        super().delete(*args, **kwargs)
        self.follower.update_following_count()
        self.following.update_follower_count()

class Retweets(models.Model):
    """Modelo para representar o relacionamento de retweets entre tweets."""

    retweeted_tweet = models.ForeignKey(
        Tweet, related_name="retweets", on_delete=models.CASCADE
    )
    retweeted_by = models.ForeignKey(
        Tweet, related_name="retweets_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Retweet"
        verbose_name_plural = "Retweets"
        unique_together = ("retweeted_tweet", "retweeted_by")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.retweeted_by} retweeted {self.retweeted_tweet}"