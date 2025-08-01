# Generated by Django 5.1.7 on 2025-08-01 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='expertprofile',
            name='category',
            field=models.CharField(choices=[('technology', 'Technology'), ('business', 'Business'), ('health', 'Health & Wellness'), ('education', 'Education'), ('finance', 'Finance'), ('marketing', 'Marketing'), ('design', 'Design & Creative'), ('science', 'Science'), ('environment', 'Environment'), ('psychology', 'Psychology'), ('legal', 'Legal'), ('real_estate', 'Real Estate'), ('fitness', 'Fitness & Sports'), ('cooking', 'Cooking & Food'), ('travel', 'Travel'), ('fashion', 'Fashion & Beauty'), ('music', 'Music & Arts'), ('parenting', 'Parenting'), ('career', 'Career Development'), ('spirituality', 'Spirituality')], default='technology', max_length=20),
        ),
        migrations.AddField(
            model_name='podcastprofile',
            name='category',
            field=models.CharField(choices=[('technology', 'Technology'), ('business', 'Business'), ('health', 'Health & Wellness'), ('education', 'Education'), ('finance', 'Finance'), ('marketing', 'Marketing'), ('design', 'Design & Creative'), ('science', 'Science'), ('environment', 'Environment'), ('psychology', 'Psychology'), ('legal', 'Legal'), ('real_estate', 'Real Estate'), ('fitness', 'Fitness & Sports'), ('cooking', 'Cooking & Food'), ('travel', 'Travel'), ('fashion', 'Fashion & Beauty'), ('music', 'Music & Arts'), ('parenting', 'Parenting'), ('career', 'Career Development'), ('spirituality', 'Spirituality')], default='technology', max_length=20),
        ),
    ]
