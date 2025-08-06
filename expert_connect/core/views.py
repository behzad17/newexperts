from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from .forms import CustomUserCreationForm, ExpertProfileForm, PodcastProfileForm, CommentForm, MessageForm
from .models import User, ExpertProfile, PodcastProfile, Like, Favorite, Comment, Message

def home(request):
    featured_experts = ExpertProfile.objects.filter(featured=True)[:6]
    featured_podcasts = PodcastProfile.objects.filter(featured=True)[:6]
    
    # Add likes count to featured experts
    for expert in featured_experts:
        content_type = ContentType.objects.get_for_model(ExpertProfile)
        expert.likes_count = Like.objects.filter(content_type=content_type, object_id=expert.pk).count()
    
    # Add likes count to featured podcasts
    for podcast in featured_podcasts:
        content_type = ContentType.objects.get_for_model(PodcastProfile)
        podcast.likes_count = Like.objects.filter(content_type=content_type, object_id=podcast.pk).count()
    
    context = {
        "featured_experts": featured_experts,
        "featured_podcasts": featured_podcasts,
    }
    return render(request, "home.html", context)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User must verify email before activation
            user.save()
            
            # Create email address record for allauth
            from allauth.account.models import EmailAddress
            email_address = EmailAddress.objects.create(
                user=user,
                email=user.email,
                primary=True,
                verified=False
            )
            
            # Create email confirmation object with proper key generation
            from allauth.account.models import EmailConfirmation
            from allauth.account.utils import generate_emailconfirmation_key
            email_confirmation = EmailConfirmation.objects.create(
                email_address=email_address,
                key=generate_emailconfirmation_key()
            )
            
            # Send email verification using allauth's adapter
            from allauth.account.adapter import get_adapter
            adapter = get_adapter()
            
            # Create a request with site information
            from django.contrib.sites.models import Site
            request.site = Site.objects.get_current()
            
            # Send confirmation email with the EmailConfirmation object
            adapter.send_confirmation_mail(request, email_confirmation, signup=True)
            
            messages.success(
                request, 
                "Registration successful! Please check your email to verify "
                "your account before logging in."
            )
            return redirect("account_login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def create_profile(request):
    if request.user.user_type == "expert":
        form_class = ExpertProfileForm
        profile_class = ExpertProfile
    else:
        form_class = PodcastProfileForm
        profile_class = PodcastProfile

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("home")
    else:
        form = form_class()
    return render(request, "create_profile.html", {"form": form})

def profile_list(request):
    experts = ExpertProfile.objects.all()
    podcasts = PodcastProfile.objects.all()
    return render(request, "profile_list.html", {"experts": experts, "podcasts": podcasts})


def experts_list(request):
    experts = ExpertProfile.objects.all()
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
    podcasts = PodcastProfile.objects.all()
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
    if user.user_type == "expert":
        profile = get_object_or_404(ExpertProfile, user=user)
    else:
        profile = get_object_or_404(PodcastProfile, user=user)

    content_type = ContentType.objects.get_for_model(profile.__class__)
    likes = Like.objects.filter(content_type=content_type, object_id=profile.pk).count()
    favorites = Favorite.objects.filter(content_type=content_type, object_id=profile.pk).count()
    comments = Comment.objects.filter(content_type=content_type, object_id=profile.pk)
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
    user = get_object_or_404(User, id=user_id)
    if user.user_type == "expert":
        profile = get_object_or_404(ExpertProfile, user=user)
    else:
        profile = get_object_or_404(PodcastProfile, user=user)

    content_type = ContentType.objects.get_for_model(profile.__class__)
    like, created = Like.objects.get_or_create(user=request.user, content_type=content_type, object_id=profile.pk)
    if not created:
        like.delete()
    return JsonResponse({"likes": Like.objects.filter(content_type=content_type, object_id=profile.pk).count()})

@login_required
def favorite_toggle(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.user_type == "expert":
        profile = get_object_or_404(ExpertProfile, user=user)
    else:
        profile = get_object_or_404(PodcastProfile, user=user)

    content_type = ContentType.objects.get_for_model(profile.__class__)
    favorite, created = Favorite.objects.get_or_create(user=request.user, content_type=content_type, object_id=profile.pk)
    if not created:
        favorite.delete()
    return JsonResponse({"favorites": Favorite.objects.filter(content_type=content_type, object_id=profile.pk).count()})

@login_required
def add_comment(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.user_type == "expert":
        profile = get_object_or_404(ExpertProfile, user=user)
    else:
        profile = get_object_or_404(PodcastProfile, user=user)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_object = profile
            comment.save()
    return redirect("profile_detail", user_id=user_id)

@login_required
def inbox(request):
    # Get all users that the current user has had a conversation with
    users = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()
    return render(request, "inbox.html", {"users": users})

@login_required
def conversation_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by("sent_at")

    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user).update(read_at=timezone.now())

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect("conversation_detail", user_id=user_id)
    else:
        form = MessageForm(initial={"receiver": other_user})

    return render(request, "conversation_detail.html", {"other_user": other_user, "messages": messages, "form": form})

@login_required
def send_message(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect("conversation_detail", user_id=user_id)
    else:
        form = MessageForm()
    
    context = {
        "form": form,
        "recipient": recipient,
    }
    return render(request, "send_message.html", context)


# Profile Management Views
@login_required
def edit_profile(request):
    """Allow users to edit their own profile"""
    try:
        if request.user.user_type == "expert":
            profile = ExpertProfile.objects.get(user=request.user)
            form_class = ExpertProfileForm
        else:
            profile = PodcastProfile.objects.get(user=request.user)
            form_class = PodcastProfileForm
    except (ExpertProfile.DoesNotExist, PodcastProfile.DoesNotExist):
        return redirect("create_profile")
    
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_detail", user_id=request.user.id)
    else:
        form = form_class(instance=profile)
    
    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "edit_profile.html", context)


@login_required
def delete_profile(request):
    """Allow users to delete their own profile"""
    try:
        if request.user.user_type == "expert":
            profile = ExpertProfile.objects.get(user=request.user)
        else:
            profile = PodcastProfile.objects.get(user=request.user)
    except (ExpertProfile.DoesNotExist, PodcastProfile.DoesNotExist):
        return redirect("home")
    
    if request.method == "POST":
        # Delete the profile
        profile.delete()
        # Optionally delete the user account as well
        # request.user.delete()
        return redirect("home")
    
    context = {
        "profile": profile,
    }
    return render(request, "delete_profile.html", context)


# Comment Management Views
@login_required
def edit_comment(request, comment_id):
    """Allow users to edit their own comments"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user owns this comment
    if comment.user != request.user:
        return redirect("profile_detail", user_id=comment.content_object.user.id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("profile_detail", user_id=comment.content_object.user.id)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        "form": form,
        "comment": comment,
    }
    return render(request, "edit_comment.html", context)


@login_required
def delete_comment(request, comment_id):
    """Allow users to delete their own comments"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user owns this comment
    if comment.user != request.user:
        return redirect("profile_detail", user_id=comment.content_object.user.id)
    
    if request.method == "POST":
        # Store the profile user ID before deleting the comment
        profile_user_id = comment.content_object.user.id
        comment.delete()
        return redirect("profile_detail", user_id=profile_user_id)
    
    context = {
        "comment": comment,
    }
    return render(request, "delete_comment.html", context)
