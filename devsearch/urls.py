from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'), name='ResetPassword'),
    path('reset_password_sent/', auth_views.PasswordChangeDoneView.as_view(template_name='users/reset_password_sent.html'), name='ResetPasswordSent'),
    path('reset_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/reset_password_confirm.html'), name='ResetPasswordConfirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password_complete.html'), name='ResetPasswordComplete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

