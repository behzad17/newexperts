from django.contrib import admin
from .models import User, ExpertProfile, PodcastProfile, Like, Favorite, Comment, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'featured', 'is_approved', 'has_image', 'created_at')
    list_filter = ('featured', 'category', 'is_approved')
    search_fields = ('name', 'bio', 'user__username', 'user__email')
    list_editable = ('featured', 'category', 'is_approved')
    actions = ['approve_profiles', 'reject_profiles', 'make_featured', 'remove_featured']
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def created_at(self, obj):
        return obj.user.date_joined
    created_at.short_description = 'Created'
    
    def approve_profiles(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} expert(s) approved successfully.')
    approve_profiles.short_description = "Approve selected experts"
    
    def reject_profiles(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} expert(s) rejected.')
    reject_profiles.short_description = "Reject selected experts"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} expert(s) marked as featured.')
    make_featured.short_description = "Mark selected experts as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f'{updated} expert(s) removed from featured.')
    remove_featured.short_description = "Remove selected experts from featured"


@admin.register(PodcastProfile)
class PodcastProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'featured', 'is_approved', 'has_image', 'created_at')
    list_filter = ('featured', 'category', 'is_approved')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    list_editable = ('featured', 'category', 'is_approved')
    actions = ['approve_profiles', 'reject_profiles', 'make_featured', 'remove_featured']
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def created_at(self, obj):
        return obj.user.date_joined
    created_at.short_description = 'Created'
    
    def approve_profiles(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} podcast(s) approved successfully.')
    approve_profiles.short_description = "Approve selected podcasts"
    
    def reject_profiles(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} podcast(s) rejected.')
    reject_profiles.short_description = "Reject selected podcasts"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} podcast(s) marked as featured.')
    make_featured.short_description = "Mark selected podcasts as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f'{updated} podcast(s) removed from featured.')
    remove_featured.short_description = "Remove selected podcasts from featured"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'text', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username', 'text')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject', 'sent_at')
    list_filter = ('sent_at',)
    search_fields = ('sender__username', 'receiver__username', 'subject', 'body')
