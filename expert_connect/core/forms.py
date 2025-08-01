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
        fields = ["name", "bio"]

class PodcastProfileForm(forms.ModelForm):
    class Meta:
        model = PodcastProfile
        fields = ["name", "description"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["receiver", "subject", "body"]
