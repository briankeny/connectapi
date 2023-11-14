from django.urls import path
from authentication import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView
    ,TokenRefreshView
)
app_name = 'authentication'
urlpatterns = [
    
    # Authentication & password reset urls 
    path('login/', TokenObtainPairView.as_view(), name='app-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
 
    # Users endpoints
    path('profile/', views.EmpList.as_view(), name='single-User-data'),
    path('Users/', views.UserList.as_view(), name='Users-list'),
    path('User/(?P<username>\w+)/', views.UserDetail.as_view(), name='User-detail')
]
