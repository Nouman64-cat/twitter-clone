from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile , Tweet, AuthUser
#unregister
admin.site.unregister(Group)

#mix profiles into user info
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

#extend user model
class UserAdmin(admin.ModelAdmin):
    model = AuthUser

    fields = ['username']
    inlines = [ProfileInline]

from django.utils.html import format_html

class TweetAdmin(admin.ModelAdmin):
    model = Tweet
    list_display = ['title', 'tweet', 'user', 'display_image', 'date_created', 'date_modified']
    fields = ['title', 'tweet', 'user', 'image', 'date_created', 'date_modified']
    readonly_fields = ['date_created', 'date_modified']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "-"
    display_image.short_description = 'Image'



#unregister user

#reregister user and profile
admin.site.register(AuthUser, UserAdmin)
#admin.site.register(Profile)

#register tweets in the admin panel
admin.site.register(Tweet, TweetAdmin)
