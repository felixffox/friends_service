from django.contrib import admin

from .models import Friendship, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username'
    )
    search_fields = ('username',)
    save_on_top = True


class FriendshipAdmin(admin.ModelAdmin):
    list_display = (
        'friend',
        'second_friend',
        'status'
    )
    search_fields = ('friend', 'second_friend')
    save_on_top = True


admin.site.register(User, UserAdmin)
admin.site.register(Friendship, FriendshipAdmin)
