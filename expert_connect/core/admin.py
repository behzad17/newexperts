from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ExpertProfile, PodcastProfile, Like, Favorite, Comment


@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'featured', 'has_image', 'has_email', 'has_website', 'created_at')
    list_filter = ('featured', 'category')
    search_fields = ('name', 'bio', 'user__username', 'user__email', 'email', 'website_url')
    list_editable = ('featured', 'category')
    actions = ['make_featured', 'remove_featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'bio', 'category', 'image')
        }),
        ('Contact Information', {
            'fields': ('email', 'website_url'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('featured',),
            'classes': ('collapse',)
        }),
    )
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def has_email(self, obj):
        return bool(obj.email)
    has_email.boolean = True
    has_email.short_description = 'Has Email'
    
    def has_website(self, obj):
        return bool(obj.website_url)
    has_website.boolean = True
    has_website.short_description = 'Has Website'
    
    def created_at(self, obj):
        return obj.user.date_joined
    created_at.short_description = 'Created'
    
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
    list_display = ('name', 'user', 'category', 'featured', 'has_image', 'created_at')
    list_filter = ('featured', 'category')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    list_editable = ('featured', 'category')
    actions = ['make_featured', 'remove_featured']
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def created_at(self, obj):
        return obj.user.date_joined
    created_at.short_description = 'Created'
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} podcast(s) marked as featured.')
    make_featured.short_description = "Mark selected podcasts as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f'{updated} podcast(s) removed from featured.')
    remove_featured.short_description = "Remove selected podcasts from featured"


admin.site.register(User, UserAdmin)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Comment)
