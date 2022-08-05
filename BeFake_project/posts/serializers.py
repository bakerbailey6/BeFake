from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MessageModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageModel
        fields = ['receiver_user', 'sender_user', 'body', 'date']
