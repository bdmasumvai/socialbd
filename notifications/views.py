from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    notifications.update(is_read=True)
    return render(request, 'notifications/notifications.html', {'notifications': notifications})
