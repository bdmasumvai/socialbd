from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from friends.models import Friendship
from django.db.models import Q


@login_required
def feed_view(request):
    # Get friends
    friendships = Friendship.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status='accepted'
    )
    friend_ids = []
    for f in friendships:
        friend_ids.append(f.receiver.id if f.sender == request.user else f.sender.id)

    friend_ids.append(request.user.id)

    posts = Post.objects.filter(
        Q(user__id__in=friend_ids, privacy__in=['public', 'friends']) |
        Q(user=request.user)
    ).select_related('user').prefetch_related('likes', 'comments')

    post_form = PostForm()
    comment_form = CommentForm()

    # Friend suggestions
    existing = list(friend_ids)
    suggestions = request.user.__class__.objects.exclude(id__in=existing).order_by('?')[:5]

    context = {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form,
        'suggestions': suggestions,
    }
    return render(request, 'feed/feed.html', context)


@login_required
@require_POST
def create_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
    return redirect('feed')


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('feed')


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        # Create notification
        if post.user != request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=post.user,
                sender=request.user,
                notification_type='like',
                post=post
            )
    return JsonResponse({'liked': liked, 'count': post.get_likes_count()})


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content', '').strip()
    if content:
        comment = Comment.objects.create(post=post, user=request.user, content=content)
        if post.user != request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=post.user,
                sender=request.user,
                notification_type='comment',
                post=post
            )
        return JsonResponse({
            'success': True,
            'username': request.user.get_full_name() or request.user.username,
            'avatar': request.user.get_profile_picture(),
            'content': comment.content,
            'time': comment.created_at.strftime('%d %b'),
            'count': post.get_comments_count()
        })
    return JsonResponse({'success': False})
