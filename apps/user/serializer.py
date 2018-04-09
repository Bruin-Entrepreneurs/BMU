from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_pic_url',
            'email',
            'bio',
            'facebook_id',
            'notification_token'
        )


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_pic_url',
        )
