# Admin Email Notifications Setup Guide

## Overview

Your Expert Connect project now includes comprehensive admin email notifications that will automatically notify you (as an admin) when important events occur on your platform.

## What You'll Receive Notifications For

### ✅ **User Registration**

- New user account creation
- User type (expert/podcast)
- Registration date and time

### ✅ **Profile Creation**

- New expert profile creation
- New podcast profile creation
- Profile details and category

### ✅ **User Activity**

- New comments posted on profiles
- New messages sent between users
- Profile deletions

### ✅ **Content Moderation**

- All new content for review
- User interactions to monitor

## Current Configuration

### Email Settings

```python
# Current setup (development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ADMIN_EMAIL = 'admin@expertconnect.com'
```

### Notification Events

- **User Registration**: ✅ Active
- **Expert Profile Creation**: ✅ Active
- **Podcast Profile Creation**: ✅ Active
- **New Comments**: ✅ Active
- **New Messages**: ✅ Active
- **Profile Deletions**: ✅ Active

## Setup Instructions

### 1. Update Your Admin Email

Edit your `.env` file:

```bash
# Admin email for notifications
ADMIN_EMAIL=your-actual-email@gmail.com
```

### 2. Choose Your Email Provider

#### Option A: Gmail (Recommended for testing)

```bash
# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=your-email@gmail.com
```

#### Option B: SendGrid (Recommended for production)

```bash
# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=verified-sender@yourdomain.com
ADMIN_EMAIL=your-email@gmail.com
```

### 3. Test the Notifications

#### Development Testing (Console Backend)

1. Start the server: `python3 manage.py runserver`
2. Register a new user
3. Create a profile
4. Add a comment
5. Check your terminal for notification emails

#### Production Testing (SMTP Backend)

1. Update your `.env` with real email credentials
2. Restart the server
3. Perform the same actions as above
4. Check your email inbox

## Sample Notification Emails

### New User Registration

```
Subject: [Expert Connect] New User Registration: john_doe

New user has registered:

Username: john_doe
Email: john@example.com
User Type: expert
Date Joined: 2025-08-05 12:30:00

View in admin: http://127.0.0.1:8000/admin/auth/user/123/
```

### New Expert Profile

```
Subject: [Expert Connect] New Expert Profile Created: John Doe

New expert profile has been created:

Name: John Doe
Category: Technology
User: john_doe (john@example.com)
Bio: Experienced software developer with 10+ years...

View in admin: http://127.0.0.1:8000/admin/core/expertprofile/456/
```

### New Comment

```
Subject: [Expert Connect] New Comment on John Doe

New comment has been posted:

Profile: John Doe
Commenter: jane_smith (jane@example.com)
Comment: Great profile! I'd love to connect...

View in admin: http://127.0.0.1:8000/admin/core/comment/789/
```

## Customization Options

### 1. Modify Notification Content

Edit `expert_connect/core/signals.py` to customize:

- Email subject lines
- Message content
- Information included in notifications

### 2. Add New Notification Types

Add new signal handlers for:

- Profile updates
- User login attempts
- System errors
- Custom events

### 3. Multiple Admin Recipients

Update the signals to send to multiple admins:

```python
ADMIN_EMAILS = [
    'admin1@expertconnect.com',
    'admin2@expertconnect.com',
    'moderator@expertconnect.com'
]

# In signal functions:
recipient_list=ADMIN_EMAILS
```

### 4. Conditional Notifications

Add conditions to only send notifications for specific events:

```python
@receiver(post_save, sender=Comment)
def notify_admin_new_comment(sender, instance, created, **kwargs):
    if created and len(instance.text) > 100:  # Only long comments
        # Send notification
```

## Email Templates (Optional)

### Create Custom Email Templates

Create `templates/admin_notifications/` directory:

#### `templates/admin_notifications/new_user.html`

```html
<!DOCTYPE html>
<html>
  <head>
    <title>New User Registration</title>
  </head>
  <body>
    <h2>New User Registration</h2>
    <p><strong>Username:</strong> {{ user.username }}</p>
    <p><strong>Email:</strong> {{ user.email }}</p>
    <p><strong>User Type:</strong> {{ user.user_type }}</p>
    <p><strong>Date Joined:</strong> {{ user.date_joined }}</p>

    <a href="{{ admin_url }}">View in Admin</a>
  </body>
</html>
```

## Troubleshooting

### Common Issues

#### 1. No emails being sent

- Check `EMAIL_BACKEND` setting
- Verify `ADMIN_EMAIL` is set correctly
- Check email provider credentials

#### 2. Emails going to spam

- Use a verified sender email
- Set up SPF/DKIM records
- Use a reputable email provider

#### 3. Too many notifications

- Add filters to signal handlers
- Implement notification preferences
- Use digest emails instead of individual notifications

### Testing Commands

#### Test Email Configuration

```python
# In Django shell
python3 manage.py shell

>>> from django.core.mail import send_mail
>>> from django.conf import settings
>>> send_mail(
...     'Test Admin Notification',
...     'This is a test email from Expert Connect.',
...     settings.DEFAULT_FROM_EMAIL,
...     [settings.ADMIN_EMAIL],
...     fail_silently=False,
... )
```

#### Check Signal Registration

```python
# In Django shell
>>> from django.db.models.signals import post_save
>>> from core.models import ExpertProfile
>>> print(len(post_save.receivers))  # Should be > 0
```

## Security Considerations

### 1. Email Security

- Use TLS/SSL for email transmission
- Store email credentials securely
- Use app passwords for Gmail

### 2. Privacy

- Don't include sensitive user data in notifications
- Consider GDPR compliance for EU users
- Implement notification preferences

### 3. Rate Limiting

- Implement email rate limiting
- Use digest emails for high-volume events
- Monitor email sending quotas

## Production Checklist

- [ ] Set up production email backend (SMTP)
- [ ] Configure admin email address
- [ ] Test all notification types
- [ ] Set up email monitoring
- [ ] Configure email templates (optional)
- [ ] Implement notification preferences
- [ ] Set up email logs
- [ ] Monitor email delivery rates

## Current Status

✅ **Admin notifications are active and working!**

- All notification types are configured
- Signals are properly registered
- Console backend shows notifications in terminal
- Ready for production email setup

**Next Steps:**

1. Update `ADMIN_EMAIL` in your `.env` file
2. Choose and configure your email provider
3. Test the notification system
4. Customize notification content if needed

## Support

- **Django Signals Documentation**: [https://docs.djangoproject.com/en/stable/topics/signals/](https://docs.djangoproject.com/en/stable/topics/signals/)
- **Django Email Documentation**: [https://docs.djangoproject.com/en/stable/topics/email/](https://docs.djangoproject.com/en/stable/topics/email/)
- **Email Provider Guides**: See `EMAIL_VERIFICATION_GUIDE.md` for setup instructions
