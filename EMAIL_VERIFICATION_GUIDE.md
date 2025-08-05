# Email Verification Setup Guide

## Current Status

✅ **Email verification is configured and working!** Here's what's currently set up:

### Configuration

- **Email verification**: `mandatory` (users must verify email before login)
- **Email backend**: `console` (emails appear in terminal for development)
- **From email**: `noreply@expertconnect.com`
- **Server email**: `server@expertconnect.com`

## How Email Verification Works

### 1. User Registration Process

1. User fills out registration form
2. User account is created but marked as `inactive`
3. Verification email is sent automatically
4. User clicks verification link in email
5. Account becomes `active` and user can login

### 2. Current Development Setup

- **Console Backend**: All emails are printed to the terminal
- **No real email sending**: Perfect for development/testing
- **Instant verification**: You can see verification links immediately

## Testing Email Verification

### 1. Start the Server

```bash
python3 manage.py runserver
```

### 2. Register a New User

1. Go to `http://127.0.0.1:8000/register/`
2. Fill out the registration form
3. Submit the form

### 3. Check the Terminal

You'll see something like this in your terminal:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: [Expert Connect] Please Confirm Your E-mail Address
From: noreply@expertconnect.com
To: user@example.com
Date: Mon, 05 Aug 2025 11:30:00 -0000
Message-ID: <20250805113000.12345@localhost>

Hello from Expert Connect!

You're receiving this e-mail because user user@example.com has given this site an e-mail address to confirm their account.

To confirm this is correct, go to http://127.0.0.1:8000/accounts/confirm-email/MQ:1abc123def456ghi789jkl/

Thank you from Expert Connect!
```

### 4. Click the Verification Link

Copy the verification link from the terminal and paste it in your browser to verify the account.

## Production Email Setup

### Option 1: Gmail SMTP (Recommended for small projects)

#### 1. Enable 2-Factor Authentication

1. Go to your Google Account settings
2. Enable 2-Factor Authentication

#### 2. Generate App Password

1. Go to Google Account → Security → App passwords
2. Generate a new app password for "Mail"
3. Copy the 16-character password

#### 3. Update .env File

```bash
# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
SERVER_EMAIL=your-email@gmail.com
```

### Option 2: SendGrid (Recommended for production)

#### 1. Create SendGrid Account

1. Sign up at [sendgrid.com](https://sendgrid.com/)
2. Verify your domain
3. Get your API key

#### 2. Install SendGrid

```bash
pip install sendgrid
```

#### 3. Update .env File

```bash
# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=verified-sender@yourdomain.com
SERVER_EMAIL=verified-sender@yourdomain.com
```

### Option 3: AWS SES (For AWS users)

#### 1. Set up AWS SES

1. Go to AWS SES console
2. Verify your email address
3. Get SMTP credentials

#### 2. Update .env File

```bash
# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
DEFAULT_FROM_EMAIL=verified-sender@yourdomain.com
SERVER_EMAIL=verified-sender@yourdomain.com
```

## Email Verification Settings

### Current Settings (in settings.py)

```python
# django-allauth Account Settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Options: 'mandatory', 'optional', 'none'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_PASSWORD_MIN_LENGTH = 8
```

### Available Options

#### ACCOUNT_EMAIL_VERIFICATION

- **'mandatory'**: User must verify email before login
- **'optional'**: User can login without verification, but email is sent
- **'none'**: No email verification

#### ACCOUNT_EMAIL_REQUIRED

- **True**: Email is required during registration
- **False**: Email is optional

## Customizing Email Templates

### 1. Create Custom Templates

Create these files in your templates directory:

```
templates/
└── account/
    ├── email/
    │   ├── email_confirmation_message.txt
    │   └── email_confirmation_subject.txt
    └── email_confirm.html
```

### 2. Example Custom Email Template

**`templates/account/email/email_confirmation_subject.txt`**:

```
[Expert Connect] Please Confirm Your Email Address
```

**`templates/account/email/email_confirmation_message.txt`**:

```
Hello from Expert Connect!

You're receiving this email because {{ user_display }} has given this site an email address to confirm their account.

To confirm this is correct, go to {{ activate_url }}

Thank you from Expert Connect!
{{ current_site.name }}
```

## Troubleshooting

### Common Issues

#### 1. "Email verification required" but no email sent

- Check your terminal for the email (console backend)
- Verify EMAIL_BACKEND is set correctly
- Check DEFAULT_FROM_EMAIL is set

#### 2. Gmail SMTP errors

- Ensure 2-Factor Authentication is enabled
- Use App Password, not regular password
- Check "Less secure app access" is disabled

#### 3. SendGrid errors

- Verify your domain in SendGrid
- Check API key permissions
- Ensure sender email is verified

#### 4. AWS SES errors

- Verify sender email address
- Check SES is out of sandbox mode
- Verify SMTP credentials

### Testing Commands

#### Test Email Configuration

```python
# In Django shell
python3 manage.py shell

>>> from django.core.mail import send_mail
>>> send_mail(
...     'Test Email',
...     'This is a test email from Expert Connect.',
...     'noreply@expertconnect.com',
...     ['test@example.com'],
...     fail_silently=False,
... )
```

#### Check Email Settings

```python
# In Django shell
>>> from django.conf import settings
>>> print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
>>> print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
>>> print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
```

## Security Best Practices

### 1. Email Security

- Use TLS/SSL for email transmission
- Use app passwords for Gmail
- Verify sender domains
- Monitor email delivery rates

### 2. Verification Security

- Use secure verification links
- Set appropriate expiration times
- Rate limit verification attempts
- Log verification activities

### 3. Production Checklist

- [ ] Use production email backend (SMTP)
- [ ] Verify sender email address
- [ ] Set up email monitoring
- [ ] Configure email templates
- [ ] Test email delivery
- [ ] Set up email logs

## Current Status Summary

✅ **Email verification is working!**

- Users must verify email before login
- Verification emails are sent automatically
- Console backend shows emails in terminal
- Ready for production email setup

**Next Steps:**

1. Test registration and verification flow
2. Choose production email provider
3. Update .env with production credentials
4. Customize email templates if needed
