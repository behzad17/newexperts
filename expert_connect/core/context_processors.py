from .models import ExpertProfile, PodcastProfile

def profile_status(request):
    """
    Context processor to add profile status information to all templates.
    This helps determine if a user has created a profile or not.
    """
    context = {}
    
    if request.user.is_authenticated:
        # Check if user has an expert profile
        has_expert_profile = ExpertProfile.objects.filter(user=request.user).exists()
        # Check if user has a podcast profile
        has_podcast_profile = PodcastProfile.objects.filter(user=request.user).exists()
        # User has a profile if they have either type
        has_profile = has_expert_profile or has_podcast_profile
        
        context.update({
            'has_expert_profile': has_expert_profile,
            'has_podcast_profile': has_podcast_profile,
            'has_profile': has_profile,
        })
    
    return context 