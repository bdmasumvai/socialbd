from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import User
from friends.models import Friendship
from django.db.models import Q


def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'স্বাগতম {user.first_name}! SocialBD-তে আপনাকে স্বাগতম।')
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, 'ভুল username বা password।')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.post_set.all().order_by('-created_at')

    friendship_status = None
    if request.user != profile_user:
        friendship = Friendship.objects.filter(
            Q(sender=request.user, receiver=profile_user) |
            Q(sender=profile_user, receiver=request.user)
        ).first()
        if friendship:
            friendship_status = friendship.status
            if friendship.status == 'pending' and friendship.receiver == request.user:
                friendship_status = 'received'

    friends = Friendship.objects.filter(
        Q(sender=profile_user) | Q(receiver=profile_user),
        status='accepted'
    )[:6]

    friend_list = []
    for f in friends:
        friend_list.append(f.receiver if f.sender == profile_user else f.sender)

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'friendship_status': friendship_status,
        'friends': friend_list,
    }
    return render(request, 'profile/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'প্রোফাইল আপডেট হয়েছে!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile/edit_profile.html', {'form': form})


@login_required
def search_view(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)
    return render(request, 'accounts/search.html', {'users': users, 'query': query})
