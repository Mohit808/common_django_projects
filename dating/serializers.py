from rest_framework import serializers
from dating.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDating
        fields = "__all__"
