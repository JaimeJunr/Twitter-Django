from django.contrib import admin
from .models import Tweet, User, Follow, Retweets

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "is_retweet", "original_tweet")

    def retweet_count(self, obj):
        return Retweets.objects.filter(retweeted_tweet=obj).count()
    retweet_count.short_description = 'Retweets'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "bio", "follower_count", "following_count")

    def follower_count(self, obj):
        return obj.followers.count()
    follower_count.short_description = 'Followers'

    def following_count(self, obj):
        return obj.followings.count()
    following_count.short_description = 'Following'

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following")

@admin.register(Retweets)
class RetweetsAdmin(admin.ModelAdmin):
    list_display = ("id", "retweeted_tweet", "retweeted_by", "created_at")