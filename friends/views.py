from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Friendship
from django.db.models import Q
from notifications.models import Notification


@login_required
@require_POST
def send_friend_request(request, user_id):
    from accounts.models import User
    receiver = get_object_or_404(User, id=user_id)
    if receiver != request.user:
        friendship, created = Friendship.objects.get_or_create(
            sender=request.user, receiver=receiver
        )
        if created:
            Notification.objects.create(
                recipient=receiver,
                sender=request.user,
                notification_type='friend_request'
            )
    return JsonResponse({'status': 'sent'})


@login_required
@require_POST
def accept_friend_request(request, user_id):
    from accounts.models import User
    sender = get_object_or_404(User, id=user_id)
    friendship = get_object_or_404(Friendship, sender=sender, receiver=request.user, status='pending')
    friendship.status = 'accepted'
    friendship.save()
    Notification.objects.create(
        recipient=sender,
        sender=request.user,
        notification_type='friend_accepted'
    )
    return JsonResponse({'status': 'accepted'})


@login_required
@require_POST
def reject_friend_request(request, user_id):
    from accounts.models import User
    sender = get_object_or_404(User, id=user_id)
    friendship = get_object_or_404(Friendship, sender=sender, receiver=request.user, status='pending')
    friendship.delete()
    return JsonResponse({'status': 'rejected'})


@login_required
@require_POST
def unfriend(request, user_id):
    from accounts.models import User
    other = get_object_or_404(User, id=user_id)
    Friendship.objects.filter(
        Q(sender=request.user, receiver=other) | Q(sender=other, receiver=request.user)
    ).delete()
    return JsonResponse({'status': 'unfriended'})


@login_required
def friend_requests_view(request):
    requests_received = Friendship.objects.filter(
        receiver=request.user, status='pending'
    ).select_related('sender')
    return render(request, 'friends/friend_requests.html', {'requests': requests_received})
