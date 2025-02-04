from django.urls import path
from .projects import views as ProjectV
from .users import views as UserV
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/create-account/', UserV.createAccount, name='create_account'),
    
    path('users/', UserV.profiles),
    path('projects/<str:id>/vote/', UserV.projectVote),
    
    path('projects/', ProjectV.getProjects),
    path('projects/<str:id>/', ProjectV.getProject),
    path('projects/delete/<str:id>/', ProjectV.deleteProject),
    path('remove-tag/', ProjectV.removeTag),
]