from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile
#unregister
admin.site.unregister(Group)

#mix profiles into user info
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User

    fields = ['username']
    inlines = [ProfileInline]

#unregister user
admin.site.unregister(User)

#reregister user and profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)
