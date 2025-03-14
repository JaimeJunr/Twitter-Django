from django.contrib import admin
from .models import Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "is_retweet", "original_tweet", "retweet_content", "retweet_count")

    # Método personalizado para contar retweets
    def retweet_count(self, obj):
        return obj.retweet_count()  # Usa o método que você já criou na model
    retweet_count.short_description = 'Retweets'  # Nome amigável para o campo
