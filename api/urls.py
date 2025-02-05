from django.urls import path
from .projects import views as ProjectV
from django.contrib.auth import views as auth_views
from .users import views as UserV
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # --------------------------
    # Authentication Routes
    # --------------------------
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # --------------------------
    # Password Reset Routes
    # --------------------------
    path('users/password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('users/password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('users/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('users/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # --------------------------
    # User Actions
    # --------------------------
    path('users/create-account/', UserV.createAccount, name='create_account'),  # Create a new user account
    path('users/', UserV.profiles, name='profiles'),  # Get all user profiles
    path('users/profile/<str:id>/', UserV.profile, name='profile'),  # Get a specific user's profile by ID
    path('users/profile/', UserV.userAccount, name='user_account'),  # Get logged-in user's profile
    path('users/profile/edit/', UserV.editAccount, name='edit_account'),  # Edit logged-in user's profile
    path('users/profile/skills/', UserV.createSkill, name='create_skill'),  # Add a skill to the user's profile
    path('users/profile/skills/<str:id>/', UserV.updateSkill, name='update_skill'),  # Update a skill
    path('users/profile/skills/delete/<str:id>/', UserV.deleteSkill, name='delete_skill'),  # Delete a skill
    path('users/messages/', UserV.inbox, name='inbox'),  # Get user's messages
    path('users/messages/<str:id>/', UserV.viewMessage, name='view_message'),  # View a specific message
    path('users/messages/send/<str:receiver_id>/', UserV.sendMessage, name='send_message'),  # Send a message

    # --------------------------
    # Project Actions
    # --------------------------
    path('projects/', ProjectV.getProjects, name='get_projects'),  # Get all projects
    path('projects/<str:id>/', ProjectV.getProject, name='get_project'),  # Get a specific project
    path('projects/create/', ProjectV.createProject, name='create_project'),  # Create a new project
    path('projects/update/<str:id>/', ProjectV.updateProject, name='update_project'),  # Update a project
    path('projects/delete/<str:id>/', ProjectV.deleteProject, name='delete_project'),  # Delete a project
    path('projects/<str:id>/vote/', UserV.projectVote, name='project_vote'),  # Vote on a project
    path('projects/remove-tag/', ProjectV.removeTag, name='remove_tag'),  # Remove a tag from a project
]