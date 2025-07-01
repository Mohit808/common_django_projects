from rest_framework import serializers
from dating.models import *


class DatingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatingUser
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = DatingUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"


class LikeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDating
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = LikeDating
        fields = "__all__"


class MatchSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Match
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class StandoutSerializer(serializers.ModelSerializer):
    user_standout = UserSerializer()
    class Meta:
        model = Standout
        fields = '__all__'


class SponsoredOutingSerializer(serializers.ModelSerializer):
    # sender = UserSerializer()
    # receiver = UserSerializer()

    sender = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    
    class Meta:
        model = SponsoredOuting
        fields = '__all__'