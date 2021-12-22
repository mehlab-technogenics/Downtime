from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('credential/', views.getLoguser),
    path('websites/', views.getWebsites),
    path('my-websites/', views.getMyWebsites),
    path('users/', views.getUsers),
    path('websites/<str:pk>/', views.getWebsite),
    path('websiteHistory/<str:pk>/', views.getWebHistory),
    path('register', views.create_auth),
    path('addWebsite/', views.addWebsite),
    path('deleteWebsite/<str:pk>/', views.deleteWebsite),
   # path('projects/<str:pk>/vote/', views.projectVote),

   # path('remove-tag/', views.removeTag)
    
]
