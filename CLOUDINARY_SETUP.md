# Cloudinary Setup Guide

## Overview

This project now uses Cloudinary for hosting user-uploaded images. Cloudinary provides:

- Automatic image optimization and transformation
- CDN delivery for fast loading
- Secure cloud storage
- Image resizing and cropping on-the-fly

## Setup Instructions

### 1. Create a Cloudinary Account

1. Go to [https://cloudinary.com/](https://cloudinary.com/)
2. Sign up for a free account
3. Verify your email address

### 2. Get Your Credentials

1. Log in to your Cloudinary Dashboard
2. Go to the "Dashboard" section
3. Copy your:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

### 3. Update Configuration

1. Open `expert_connect/cloudinary_config.py`
2. Replace the placeholder values with your actual credentials:

```python
CLOUDINARY_CONFIG = {
    'CLOUD_NAME': 'your-actual-cloud-name',
    'API_KEY': 'your-actual-api-key',
    'API_SECRET': 'your-actual-api-secret',
}
```

3. Update `expert_connect/expert_connect/settings.py` with the same values:

```python
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'your-actual-cloud-name',
    'API_KEY': 'your-actual-api-key',
    'API_SECRET': 'your-actual-api-secret',
}

CLOUDINARY = {
    'cloud_name': 'your-actual-cloud-name',
    'api_key': 'your-actual-api-key',
    'api_secret': 'your-actual-api-secret',
}
```

### 4. Update Forms (Optional)

If you want to customize image transformations, update the forms in `expert_connect/core/forms.py`:

```python
image = CloudinaryFileField(
    options={
        'cloud_name': 'your-actual-cloud-name',
        'folder': 'expert_images',
        'transformation': [
            {'width': 400, 'height': 400, 'crop': 'fill'},
            {'quality': 'auto'}
        ]
    },
    required=False
)
```

### 5. Test the Integration

1. Run the Django development server: `python3 manage.py runserver`
2. Go to the admin panel: `http://127.0.0.1:8000/admin/`
3. Create or edit an expert/podcast profile
4. Upload an image
5. Check that the image appears correctly

## Features

### Automatic Image Optimization

- Images are automatically optimized for web delivery
- Multiple formats supported (WebP, AVIF, etc.)
- Automatic quality optimization

### Image Transformations

- Automatic resizing to 400x400 pixels
- Fill cropping to maintain aspect ratio
- Quality optimization

### Folder Organization

- Expert images: `expert_images/` folder
- Podcast images: `podcast_images/` folder

### Security

- Images are served via secure HTTPS
- Access control through Cloudinary settings
- No local storage of sensitive image data

## Environment Variables (Recommended)

For production, use environment variables instead of hardcoding credentials:

```python
import os

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
```

## Troubleshooting

### Common Issues

1. **"Invalid credentials" error**: Double-check your API key and secret
2. **Images not uploading**: Ensure your Cloudinary account is active
3. **Slow image loading**: Check your internet connection and Cloudinary status

### Support

- Cloudinary Documentation: [https://cloudinary.com/documentation](https://cloudinary.com/documentation)
- Django Cloudinary Storage: [https://github.com/klis87/django-cloudinary-storage](https://github.com/klis87/django-cloudinary-storage)

## Migration from Local Storage

If you have existing images in your local media folder:

1. Upload them manually to Cloudinary
2. Update the database records with the new Cloudinary URLs
3. Remove the local media folder

## Cost Considerations

- Free tier includes 25 GB storage and 25 GB bandwidth per month
- Additional usage is charged per GB
- Monitor your usage in the Cloudinary Dashboard
