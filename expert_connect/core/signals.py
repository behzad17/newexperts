from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import ExpertProfile, PodcastProfile, Comment, Message

# Admin email settings
ADMIN_EMAIL = getattr(settings, 'ADMIN_EMAIL', 'admin@expertconnect.com')

@receiver(post_save, sender=ExpertProfile)
def notify_admin_new_expert(sender, instance, created, **kwargs):
    """Notify admin when a new expert profile is created"""
    if created:
        subject = f'[Expert Connect] New Expert Profile Created: {instance.name}'
        message = f"""
New expert profile has been created:

Name: {instance.name}
Category: {instance.get_category_display()}
User: {instance.user.username} ({instance.user.email})
Bio: {instance.bio[:200]}...

View in admin: http://127.0.0.1:8000/admin/core/expertprofile/{instance.pk}/
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=True,
        )

@receiver(post_save, sender=PodcastProfile)
def notify_admin_new_podcast(sender, instance, created, **kwargs):
    """Notify admin when a new podcast profile is created"""
    if created:
        subject = f'[Expert Connect] New Podcast Profile Created: {instance.name}'
        message = f"""
New podcast profile has been created:

Name: {instance.name}
Category: {instance.get_category_display()}
User: {instance.user.username} ({instance.user.email})
Description: {instance.description[:200]}...

View in admin: http://127.0.0.1:8000/admin/core/podcastprofile/{instance.pk}/
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=True,
        )

@receiver(post_save, sender=Comment)
def notify_admin_new_comment(sender, instance, created, **kwargs):
    """Notify admin when a new comment is posted"""
    if created:
        profile_name = instance.content_object.name
        subject = f'[Expert Connect] New Comment on {profile_name}'
        message = f"""
New comment has been posted:

Profile: {profile_name}
Commenter: {instance.user.username} ({instance.user.email})
Comment: {instance.text[:200]}...

View in admin: http://127.0.0.1:8000/admin/core/comment/{instance.pk}/
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=True,
        )

@receiver(post_save, sender=Message)
def notify_admin_new_message(sender, instance, created, **kwargs):
    """Notify admin when a new message is sent"""
    if created:
        subject = f'[Expert Connect] New Message: {instance.subject}'
        message = f"""
New message has been sent:

From: {instance.sender.username} ({instance.sender.email})
To: {instance.receiver.username} ({instance.receiver.email})
Subject: {instance.subject}
Message: {instance.body[:200]}...

View in admin: http://127.0.0.1:8000/admin/core/message/{instance.pk}/
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=True,
        )

@receiver(post_save, sender=User)
def notify_admin_new_user(sender, instance, created, **kwargs):
    """Notify admin when a new user registers"""
    if created:
        subject = f'[Expert Connect] New User Registration: {instance.username}'
        message = f"""
New user has registered:

Username: {instance.username}
Email: {instance.email}
User Type: {instance.user_type}
Date Joined: {instance.date_joined}

View in admin: http://127.0.0.1:8000/admin/auth/user/{instance.pk}/
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ADMIN_EMAIL],
            fail_silently=True,
        )

# Optional: Notify admin when profiles are deleted
@receiver(post_delete, sender=ExpertProfile)
def notify_admin_expert_deleted(sender, instance, **kwargs):
    """Notify admin when an expert profile is deleted"""
    subject = f'[Expert Connect] Expert Profile Deleted: {instance.name}'
    message = f"""
Expert profile has been deleted:

Name: {instance.name}
User: {instance.user.username} ({instance.user.email})
Category: {instance.get_category_display()}

This action was performed by the user or admin.
        """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[ADMIN_EMAIL],
        fail_silently=True,
    )

@receiver(post_delete, sender=PodcastProfile)
def notify_admin_podcast_deleted(sender, instance, **kwargs):
    """Notify admin when a podcast profile is deleted"""
    subject = f'[Expert Connect] Podcast Profile Deleted: {instance.name}'
    message = f"""
Podcast profile has been deleted:

Name: {instance.name}
User: {instance.user.username} ({instance.user.email})
Category: {instance.get_category_display()}

This action was performed by the user or admin.
        """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[ADMIN_EMAIL],
        fail_silently=True,
    ) 