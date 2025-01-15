from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="Login"),
    path('logout/', views.logoutUser, name="Logout"),
    path('register/', views.registerUser, name="Register"),

    path('', views.profile, name='Profiles'),
    path('profile/<str:id>/', views.userProfile, name="UserProfile"),
    path('account/', views.userAccount, name='Account'),
    
    path('edit-account/', views.editAccount, name='EditAccount'),
    
    path('create-skill/', views.createSkill, name="CreateSkill"),
    path('delete-skill/<str:id>/', views.deleteSkill, name="DeleteSkill"),
    path('update-skill/<str:id>/', views.updateSkill, name="UpdateSkill"),
    
    path('inbox/', views.inbox, name="Inbox"),
    path('message/<str:id>/', views.viewMessage, name="Message"),
    path('send-message/<str:receiver_id>/', views.sendMessage, name="SendMessage")
    
]
