from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('friend_request', 'Friend Request'),
        ('friend_accepted', 'Friend Accepted'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.notification_type}"

    def get_message(self):
        messages = {
            'like': f'{self.sender.get_full_name() or self.sender.username} আপনার পোস্টে লাইক দিয়েছে',
            'comment': f'{self.sender.get_full_name() or self.sender.username} আপনার পোস্টে মন্তব্য করেছে',
            'friend_request': f'{self.sender.get_full_name() or self.sender.username} আপনাকে বন্ধু অনুরোধ পাঠিয়েছে',
            'friend_accepted': f'{self.sender.get_full_name() or self.sender.username} আপনার বন্ধু অনুরোধ গ্রহণ করেছে',
        }
        return messages.get(self.notification_type, '')
