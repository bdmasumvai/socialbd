from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default_avatar.png'

    def get_friends_count(self):
        from friends.models import Friendship
        return Friendship.objects.filter(
            models.Q(sender=self) | models.Q(receiver=self),
            status='accepted'
        ).count()

    def get_posts_count(self):
        return self.post_set.count()
