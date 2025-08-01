from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ExpertProfile, PodcastProfile, Like, Favorite, Comment

admin.site.register(User, UserAdmin)
admin.site.register(ExpertProfile)
admin.site.register(PodcastProfile)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Comment)
