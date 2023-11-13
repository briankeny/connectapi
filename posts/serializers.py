from rest_framework import serializers
from .models import(Post)
from rest_framework import serializers
from authentication.serializers import UserSerializer

class PostSerializerWithOwner(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = Post
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Post
        fields = '__all__'
    
        
