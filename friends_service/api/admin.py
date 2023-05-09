from django.contrib import admin

from .models import CustomUser, Friendship


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username'
    )
    search_fields = ('username',)
    save_on_top = True


class FriendshipAdmin(admin.ModelAdmin):
    list_display = (
        'initiator_friend',
        'target_friend',
        'status_friendship',
        'friendship_date'
    )
    search_fields = (
        'initiator_friend',
        'target_friend',
        'status_friendship'
    )
    save_on_top = True


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Friendship, FriendshipAdmin)
