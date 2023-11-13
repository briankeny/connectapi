import ipaddress
from django.forms import ValidationError
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.utils import timezone
import os
from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from .models import(User)
from .serializers import (UserSerializer)
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions, AllowAny,IsAdminUser



class EmpList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    parser_classes = (MultiPartParser,)
    serializer_class = UserSerializer
    lookup_field = 'pk'
    renderer_classes = [JSONRenderer]
    queryset = User.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(public_service_no=user.public_service_no)
    
    def create(self, request, *args, **kwargs):
        return Response({"message":"Unsupported Request or Method"},
                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
class UserList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'pk'
    parser_classes = (MultiPartParser,)
    renderer_classes = [JSONRenderer]
    queryset = User.objects.all()

    @permission_required('authentication.add_User')
    def create(self, request, *args, **kwargs):
        user = self.request.user
        # Check if the user is a superuser or staff to proceed 
        if not (user.is_superuser or user.is_staff):
            return Response({"detail": "You Are not Authorized to Perform This Operation"},
                             status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
             
        # Optional search term filtering
        search_term = str(self.request.query_params.get('searchTerm', None))
        search = str(self.request.query_params.get('search', None))
        queryset = User.objects.all()
        if search_term != "None" and search != "None":
            try:
                field = f'{search_term}__icontains'
                # Use filter() for case-insensitive search using icontains
                queryset = queryset.filter(**{field: search})
                queryset =queryset[:45]
            except Exception as e:
                queryset = User.objects.none()

        serializer = self.serializer_class(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK) 

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes=(MultiPartParser,)
    lookup_field = 'pk'
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all() 
        if not (user.is_superuser):
           queryset = queryset.filter(public_service_no = user.public_service_no) 
        return queryset
     
    def put(self, request, *args, **kwargs):
        return Response({"message":"Unsupported Request or Method not Allowed"},
                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    def patch(self, request, *args, **kwargs):
        # Get the person making the request from the request body
        user = self.request.user
        # Get the person referred to in this instance
        instance = self.get_object()       
        profile_picture = request.data.get('profile_picture', None)
        # Check if it is the same person or an authorized party, then proceed to make changes
        if not (instance.public_service_no == user.public_service_no or user.is_superuser): 
            return Response({"message": "You are not authorized to perform this operation"}, 
                            status=status.HTTP_403_FORBIDDEN)

        
        # User  Changing The Profile Picture
        if profile_picture:
            # Delete the existing profile_picture if it exists
            existing_profile_picture = instance.profile_picture
            if existing_profile_picture:
                path_to_existing_picture = os.path.join('media', str(existing_profile_picture))
                if os.path.exists(path_to_existing_picture):
                    try:
                        os.remove(path_to_existing_picture)
                    except Exception as e:      
                        pass
       
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

