from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from .models import User, ExpertProfile, PodcastProfile, Like, Favorite, Comment, Message
from .forms import CustomUserCreationForm, ExpertProfileForm, PodcastProfileForm, CommentForm, MessageForm


def home(request):
    # Get featured profiles that are approved
    featured_experts = ExpertProfile.objects.filter(featured=True, is_approved=True)
    featured_podcasts = PodcastProfile.objects.filter(featured=True, is_approved=True)
    
    # Add likes count to featured experts
    content_type_expert = ContentType.objects.get_for_model(ExpertProfile)
    for expert in featured_experts:
        expert.likes_count = Like.objects.filter(content_type=content_type_expert, object_id=expert.pk).count()
    
    # Add likes count to featured podcasts
    content_type_podcast = ContentType.objects.get_for_model(PodcastProfile)
    for podcast in featured_podcasts:
        podcast.likes_count = Like.objects.filter(content_type=content_type_podcast, object_id=podcast.pk).count()
    
    context = {
        "featured_experts": featured_experts,
        "featured_podcasts": featured_podcasts,
    }
    return render(request, "home.html", context)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def create_profile(request):
    if hasattr(request.user, 'expertprofile') or hasattr(request.user, 'podcastprofile'):
        messages.warning(request, "You already have a profile.")
        return redirect("home")
    
    if request.method == "POST":
        if request.user.user_type == "expert":
            form = ExpertProfileForm(request.POST, request.FILES)
        else:
            form = PodcastProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.is_approved = False  # Set to pending approval
            profile.save()
            messages.success(request, "Profile created successfully! It will be visible after admin approval.")
            return redirect("home")
    else:
        if request.user.user_type == "expert":
            form = ExpertProfileForm()
        else:
            form = PodcastProfileForm()
    
    return render(request, "create_profile.html", {"form": form})


def profile_list(request):
    # Only show approved profiles
    experts = ExpertProfile.objects.filter(is_approved=True)
    podcasts = PodcastProfile.objects.filter(is_approved=True)
    
    # Add likes count to experts
    content_type_expert = ContentType.objects.get_for_model(ExpertProfile)
    for expert in experts:
        expert.likes_count = Like.objects.filter(content_type=content_type_expert, object_id=expert.pk).count()
    
    # Add likes count to podcasts
    content_type_podcast = ContentType.objects.get_for_model(PodcastProfile)
    for podcast in podcasts:
        podcast.likes_count = Like.objects.filter(content_type=content_type_podcast, object_id=podcast.pk).count()
    
    context = {
        "experts": experts,
        "podcasts": podcasts,
    }
    return render(request, "profile_list.html", context)


def experts_list(request):
    # Only show approved experts
    experts = ExpertProfile.objects.filter(is_approved=True)
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    if category:
        experts = experts.filter(category=category)
    
    if search_query:
        experts = experts.filter(
            Q(name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Add likes count to all experts
    content_type = ContentType.objects.get_for_model(ExpertProfile)
    for expert in experts:
        expert.likes_count = Like.objects.filter(content_type=content_type, object_id=expert.pk).count()
    
    # Get all categories for the filter dropdown
    categories = ExpertProfile.CATEGORY_CHOICES
    
    context = {
        "experts": experts,
        "categories": categories,
        "selected_category": category,
        "search_query": search_query,
    }
    return render(request, "experts_list.html", context)


def podcasts_list(request):
    # Only show approved podcasts
    podcasts = PodcastProfile.objects.filter(is_approved=True)
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    if category:
        podcasts = podcasts.filter(category=category)
    
    if search_query:
        podcasts = podcasts.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Add likes count to all podcasts
    content_type = ContentType.objects.get_for_model(PodcastProfile)
    for podcast in podcasts:
        podcast.likes_count = Like.objects.filter(content_type=content_type, object_id=podcast.pk).count()
    
    # Get all categories for the filter dropdown
    categories = PodcastProfile.CATEGORY_CHOICES
    
    context = {
        "podcasts": podcasts,
        "categories": categories,
        "selected_category": category,
        "search_query": search_query,
    }
    return render(request, "podcasts_list.html", context)


def profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if hasattr(user, 'expertprofile'):
        profile = user.expertprofile
        # Only show approved profiles
        if not profile.is_approved:
            messages.error(request, "This profile is not available.")
            return redirect("home")
    elif hasattr(user, 'podcastprofile'):
        profile = user.podcastprofile
        # Only show approved profiles
        if not profile.is_approved:
            messages.error(request, "This profile is not available.")
            return redirect("home")
    else:
        messages.error(request, "Profile not found.")
        return redirect("home")
    
    # Get likes and favorites count
    content_type = ContentType.objects.get_for_model(type(profile))
    likes = Like.objects.filter(content_type=content_type, object_id=profile.pk).count()
    favorites = Favorite.objects.filter(content_type=content_type, object_id=profile.pk).count()
    
    # Get comments
    comments = Comment.objects.filter(content_type=content_type, object_id=profile.pk).order_by('-created_at')
    
    # Comment form
    comment_form = CommentForm()
    
    context = {
        "profile": profile,
        "likes": likes,
        "favorites": favorites,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "profile_detail.html", context)


@login_required
def like_toggle(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        
        if hasattr(user, 'expertprofile'):
            profile = user.expertprofile
        elif hasattr(user, 'podcastprofile'):
            profile = user.podcastprofile
        else:
            return JsonResponse({"error": "Profile not found"}, status=404)
        
        # Only allow likes on approved profiles
        if not profile.is_approved:
            return JsonResponse({"error": "Cannot like unapproved profile"}, status=403)
        
        content_type = ContentType.objects.get_for_model(type(profile))
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=profile.pk
        )
        
        if not created:
            like.delete()
        
        likes_count = Like.objects.filter(content_type=content_type, object_id=profile.pk).count()
        return JsonResponse({"likes": likes_count})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def favorite_toggle(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        
        if hasattr(user, 'expertprofile'):
            profile = user.expertprofile
        elif hasattr(user, 'podcastprofile'):
            profile = user.podcastprofile
        else:
            return JsonResponse({"error": "Profile not found"}, status=404)
        
        # Only allow favorites on approved profiles
        if not profile.is_approved:
            return JsonResponse({"error": "Cannot favorite unapproved profile"}, status=403)
        
        content_type = ContentType.objects.get_for_model(type(profile))
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=profile.pk
        )
        
        if not created:
            favorite.delete()
        
        favorites_count = Favorite.objects.filter(content_type=content_type, object_id=profile.pk).count()
        return JsonResponse({"favorites": favorites_count})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def add_comment(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        
        if hasattr(user, 'expertprofile'):
            profile = user.expertprofile
        elif hasattr(user, 'podcastprofile'):
            profile = user.podcastprofile
        else:
            messages.error(request, "Profile not found.")
            return redirect("home")
        
        # Only allow comments on approved profiles
        if not profile.is_approved:
            messages.error(request, "Cannot comment on unapproved profile.")
            return redirect("home")
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = ContentType.objects.get_for_model(type(profile))
            comment.object_id = profile.pk
            comment.save()
            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Error adding comment.")
        
        return redirect("profile_detail", user_id=user_id)
    
    return redirect("home")


@login_required
def inbox(request):
    # Get all conversations for the current user
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    received_messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    
    # Combine and sort by date
    all_messages = list(sent_messages) + list(received_messages)
    all_messages.sort(key=lambda x: x.created_at, reverse=True)
    
    context = {
        "messages": all_messages,
    }
    return render(request, "inbox.html", context)


@login_required
def send_message(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, "Message sent successfully!")
            return redirect("inbox")
    else:
        form = MessageForm()
    
    context = {
        "form": form,
        "receiver": receiver,
    }
    return render(request, "send_message.html", context)


@login_required
def conversation_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Get messages between current user and other user
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('created_at')
    
    context = {
        "messages": messages,
        "other_user": other_user,
    }
    return render(request, "conversation_detail.html", context)


@login_required
def profile_status(request):
    """Show user their profile approval status"""
    if hasattr(request.user, 'expertprofile'):
        profile = request.user.expertprofile
        profile_type = 'Expert'
    elif hasattr(request.user, 'podcastprofile'):
        profile = request.user.podcastprofile
        profile_type = 'Podcast'
    else:
        messages.warning(request, "You don't have a profile yet.")
        return redirect("create_profile")
    
    context = {
        "profile": profile,
        "profile_type": profile_type,
    }
    return render(request, "profile_status.html", context)
