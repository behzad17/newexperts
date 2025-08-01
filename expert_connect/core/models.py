from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("expert", "Expert"),
        ("podcaster", "Podcaster"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)


class ExpertProfile(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('business', 'Business'),
        ('health', 'Health & Wellness'),
        ('education', 'Education'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('design', 'Design & Creative'),
        ('science', 'Science'),
        ('environment', 'Environment'),
        ('psychology', 'Psychology'),
        ('legal', 'Legal'),
        ('real_estate', 'Real Estate'),
        ('fitness', 'Fitness & Sports'),
        ('cooking', 'Cooking & Food'),
        ('travel', 'Travel'),
        ('fashion', 'Fashion & Beauty'),
        ('music', 'Music & Arts'),
        ('parenting', 'Parenting'),
        ('career', 'Career Development'),
        ('spirituality', 'Spirituality'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technology')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PodcastProfile(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('business', 'Business'),
        ('health', 'Health & Wellness'),
        ('education', 'Education'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('design', 'Design & Creative'),
        ('science', 'Science'),
        ('environment', 'Environment'),
        ('psychology', 'Psychology'),
        ('legal', 'Legal'),
        ('real_estate', 'Real Estate'),
        ('fitness', 'Fitness & Sports'),
        ('cooking', 'Cooking & Food'),
        ('travel', 'Travel'),
        ('fashion', 'Fashion & Beauty'),
        ('music', 'Music & Arts'),
        ('parenting', 'Parenting'),
        ('career', 'Career Development'),
        ('spirituality', 'Spirituality'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technology')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content_type", "object_id")


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content_type", "object_id")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content_object}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.subject}"
