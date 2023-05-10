from rest_framework import serializers

from .models import CustomUser, Friendship


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username'
        )


class FriendshipStatusSerializer(serializers.Serializer):
    friendship_status = serializers.CharField(read_only=True)


class FriendshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = (
            'id',
            'target_friend',
            'status_friendship',
            'friendship_date'
        )
        read_only_fields = ('status_friendship',)
