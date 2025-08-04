from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ExpertProfile, PodcastProfile, Comment, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("user_type",)


class ExpertProfileForm(forms.ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ["name", "bio", "category", "image", "email", "website_url", 
                 "linkedin_url", "twitter_url", "instagram_url"]
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourwebsite.com'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/yourhandle'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/yourhandle'}),
        }


class PodcastProfileForm(forms.ModelForm):
    class Meta:
        model = PodcastProfile
        fields = ["name", "description", "category", "image"]
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
