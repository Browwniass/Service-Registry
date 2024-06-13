from rest_framework import serializers
from teams.models.user import User
from rest_framework.utils import model_meta


#Serializer of the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['role']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance