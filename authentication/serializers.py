from rest_framework import serializers
from .models import( User)
from django.contrib.auth.hashers import make_password
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  
    
    # Exclude password from serialization
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)  # Hash the password
        validated_data['password'] = hashed_password
        return super().create(validated_data)    
    class Meta:
       
        model = User
        fields = '__all__'












