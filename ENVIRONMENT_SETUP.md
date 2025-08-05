# Environment Variables Setup Guide

## Overview

This project uses environment variables to manage sensitive configuration data and settings. This approach provides better security and flexibility across different environments (development, staging, production).

## Quick Setup

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Update Your .env File

Edit the `.env` file with your actual values:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-actual-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Cloudinary Settings
CLOUDINARY_CLOUD_NAME=your-actual-cloud-name
CLOUDINARY_API_KEY=your-actual-api-key
CLOUDINARY_API_SECRET=your-actual-api-secret
```

## Environment Variables Reference

### Django Settings

| Variable        | Description                           | Default               | Required |
| --------------- | ------------------------------------- | --------------------- | -------- |
| `DEBUG`         | Enable debug mode                     | `True`                | No       |
| `SECRET_KEY`    | Django secret key                     | Auto-generated        | Yes      |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` | No       |

### Database Settings

| Variable       | Description             | Default                | Required |
| -------------- | ----------------------- | ---------------------- | -------- |
| `DATABASE_URL` | Database connection URL | `sqlite:///db.sqlite3` | No       |

### Cloudinary Settings

| Variable                | Description                | Default           | Required |
| ----------------------- | -------------------------- | ----------------- | -------- |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary cloud name | `your-cloud-name` | Yes      |
| `CLOUDINARY_API_KEY`    | Your Cloudinary API key    | `your-api-key`    | Yes      |
| `CLOUDINARY_API_SECRET` | Your Cloudinary API secret | `your-api-secret` | Yes      |

### Email Settings

| Variable              | Description                 | Default                                          | Required |
| --------------------- | --------------------------- | ------------------------------------------------ | -------- |
| `EMAIL_BACKEND`       | Email backend to use        | `django.core.mail.backends.console.EmailBackend` | No       |
| `EMAIL_HOST`          | SMTP host                   | `smtp.gmail.com`                                 | No       |
| `EMAIL_PORT`          | SMTP port                   | `587`                                            | No       |
| `EMAIL_USE_TLS`       | Use TLS encryption          | `True`                                           | No       |
| `EMAIL_HOST_USER`     | Email username              | ``                                               | No       |
| `EMAIL_HOST_PASSWORD` | Email password/app password | ``                                               | No       |

### Social Authentication Settings

| Variable               | Description                | Default                     | Required |
| ---------------------- | -------------------------- | --------------------------- | -------- |
| `GOOGLE_CLIENT_ID`     | Google OAuth client ID     | `your-google-client-id`     | No       |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | `your-google-client-secret` | No       |
| `FACEBOOK_APP_ID`      | Facebook app ID            | `your-facebook-app-id`      | No       |
| `FACEBOOK_APP_SECRET`  | Facebook app secret        | `your-facebook-app-secret`  | No       |
| `TWITTER_API_KEY`      | Twitter API key            | `your-twitter-api-key`      | No       |
| `TWITTER_API_SECRET`   | Twitter API secret         | `your-twitter-api-secret`   | No       |

### Site Settings

| Variable   | Description    | Default                 | Required |
| ---------- | -------------- | ----------------------- | -------- |
| `SITE_ID`  | Django site ID | `1`                     | No       |
| `SITE_URL` | Site URL       | `http://127.0.0.1:8000` | No       |

### Security Settings

| Variable                | Description                             | Default                                       | Required |
| ----------------------- | --------------------------------------- | --------------------------------------------- | -------- |
| `CSRF_TRUSTED_ORIGINS`  | Comma-separated list of trusted origins | `http://127.0.0.1:8000,http://localhost:8000` | No       |
| `SECURE_SSL_REDIRECT`   | Redirect HTTP to HTTPS                  | `False`                                       | No       |
| `SESSION_COOKIE_SECURE` | Secure session cookies                  | `False`                                       | No       |
| `CSRF_COOKIE_SECURE`    | Secure CSRF cookies                     | `False`                                       | No       |

### Development Settings

| Variable            | Description                 | Default | Required |
| ------------------- | --------------------------- | ------- | -------- |
| `USE_DEBUG_TOOLBAR` | Enable Django Debug Toolbar | `False` | No       |
| `LOG_LEVEL`         | Logging level               | `INFO`  | No       |

## Getting Your Credentials

### Cloudinary

1. Sign up at [https://cloudinary.com/](https://cloudinary.com/)
2. Go to your Dashboard
3. Copy your Cloud Name, API Key, and API Secret

### Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Copy Client ID and Client Secret

### Facebook OAuth

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login product
4. Copy App ID and App Secret

### Twitter OAuth

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Copy API Key and API Secret

## Production Deployment

### Environment Variables in Production

For production deployment, set environment variables in your hosting platform:

#### Heroku

```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
heroku config:set CLOUDINARY_API_KEY=your-api-key
heroku config:set CLOUDINARY_API_SECRET=your-api-secret
```

#### DigitalOcean App Platform

Add environment variables in the App Platform dashboard.

#### AWS Elastic Beanstalk

Use the EB CLI or AWS Console to set environment variables.

### Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong, unique secret keys** for production
3. **Rotate credentials regularly**
4. **Use different credentials** for development and production
5. **Limit access** to production credentials

## Troubleshooting

### Common Issues

#### 1. Environment Variables Not Loading

```bash
# Check if .env file exists
ls -la .env

# Check if python-dotenv is installed
pip list | grep python-dotenv
```

#### 2. Cloudinary Not Working

```bash
# Verify Cloudinary credentials
echo $CLOUDINARY_CLOUD_NAME
echo $CLOUDINARY_API_KEY
echo $CLOUDINARY_API_SECRET
```

#### 3. Email Not Sending

```bash
# Check email settings
echo $EMAIL_HOST
echo $EMAIL_HOST_USER
echo $EMAIL_HOST_PASSWORD
```

### Testing Environment Variables

```python
# In Django shell
python manage.py shell

>>> import os
>>> print(os.getenv('CLOUDINARY_CLOUD_NAME'))
>>> print(os.getenv('DEBUG'))
```

## File Structure

```
expert_connect/
├── .env                    # Your actual environment variables (not in git)
├── .env.example           # Template for environment variables
├── .gitignore             # Excludes .env from version control
└── expert_connect/
    └── settings.py        # Uses environment variables
```

## Support

- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Django Environment Variables](https://docs.djangoproject.com/en/stable/topics/settings/)
- [Cloudinary Documentation](https://cloudinary.com/documentation)
