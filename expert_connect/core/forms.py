from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ExpertProfile, PodcastProfile, Comment, Message
from cloudinary.forms import CloudinaryFileField
import os


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "user_type"]


class ExpertProfileForm(forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', 'your-cloud-name'),
            'folder': 'expert_images',
            'transformation': [
                {'width': 400, 'height': 400, 'crop': 'fill'},
                {'quality': 'auto'}
            ]
        },
        required=False
    )
    
    class Meta:
        model = ExpertProfile
        fields = ["name", "bio", "category", "image", "email", "website_url", 
                 "linkedin_url", "twitter_url", "instagram_url"]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourwebsite.com'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/yourhandle'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/yourhandle'}),
        }


class PodcastProfileForm(forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', 'your-cloud-name'),
            'folder': 'podcast_images',
            'transformation': [
                {'width': 400, 'height': 400, 'crop': 'fill'},
                {'quality': 'auto'}
            ]
        },
        required=False
    )
    
    class Meta:
        model = PodcastProfile
        fields = ["name", "description", "category", "image"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Message subject"}),
            "body": forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "Your message..."}),
        }
