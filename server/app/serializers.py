from rest_framework import serializers
from .models import UserModel, GameHistoryModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistoryModel
        fields = '__all__'