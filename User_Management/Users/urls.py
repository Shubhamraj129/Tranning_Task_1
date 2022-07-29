from django.urls import path, include
from .views import *

app_name = 'Users'
Profile_list = User_View.as_view({
    'get': 'list',
    'post': 'create',
})
Profile_detail = User_View.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})
urlpatterns = [
    path('activate/<int:pk>/<slug:token>/', activate),
    path('dj/', include('dj_rest_auth.urls'), name='Rest'),
    path('profile/', Profile_list, name='profile_list'),
    path('profile/<int:pk>/', Profile_detail, name='profile_Detail'),
    path('login/', CustomAuthToken.as_view(), name='login_user'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forget/', Password_reset.as_view(), name='forget'),
    path('reset_password/<int:pk>/<slug:token>/', forget_password.as_view(), name='reset_password')
]
