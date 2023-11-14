import os
import uuid
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from .models import(User,Post)
from .serializers import ( PostSerializer,PostSerializerWithOwner)
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .models import Post

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    renderer_classes=[JSONRenderer]
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializerWithOwner
        return PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        # Optional search term filtering
        search_term = self.request.query_params.get('search_Term', None)
        queryset = queryset.order_by('-timestamp')  
        if search_term:
            try:
                # Assuming 'search_term' should be an integer
                queryset = queryset.filter(owner=search_term)[:30]  # Limit results
            except ValueError:
                queryset = []  # Set the queryset to an empty list if ValueError
        
        return queryset        
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    def create(self, request, *args, **kwargs):
        owner = self.request.user
        cleaned_images = []
        index = 0 
        while  f'image_{index}' in request.data and index <4:
            name = f'image_{index}'
            current = request.data.get(name)
            path_to_img = os.path.join('media', 'post_images')
            if not os.path.exists(path_to_img):
                try:
                        os.makedirs(path_to_img)
                except Exception as e:
                    
                        pass
                # Try To Upload image to path created
            try:
                    # Generate a unique filename for the image (you may want to implement this)
                    file_ext = current.content_type
                    img_type = '.' + file_ext.split('/')[-1]
                    file_name = f'{owner.first_name}{owner.last_name}{uuid.uuid4().hex}{img_type}'
                    img_path = os.path.join(path_to_img,file_name)
                    
                    # Save the image to the specified path
                    with open(img_path, 'wb') as destination:
                        for chunk in current.chunks():
                            destination.write(chunk)
                    cleaned_images.append(file_name)

            except Exception as e:
                   
                    return Response({'error': 'Error uploading image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            index +=1

        try:    
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['owner'] = owner  # Set the owner here
            if len(cleaned_images) >0:
                serializer.validated_data['images'] = cleaned_images 
            serializer.save()

        except Exception as e:
             return Response({'error':'Try again Later'}, status=status.HTTP_400_BAD_REQUEST)
             
      
        return Response({}, status=status.HTTP_201_CREATED)
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes=[JSONRenderer]
    serializer_class = PostSerializer

    def patch(self, request, *args, **kwargs):
         return Response({'message': 'Unsupported Request.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def put(self, request, *args, **kwargs):
         return Response({'message': 'Unsupported Request.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
