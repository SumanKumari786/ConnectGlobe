"""ConnectGlobe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from Globe.views import (
        ActivateAccount,
        PostListView,
        PostDetailView,
        PostCreateView,
        PostUpdateView,
        PostDeleteView
)
from Globe import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.connect_login, name='Login'),
    path('logout/', views.logout, name='logout'),
    path('Register/', views.connect_register, name='Register'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('view/', views.view_status, name='view'),
    path('feedback/', views.feedback, name='feedback'),
    path('email_confirm_msg/', views.email_confirm_msg, name='email_confirm_msg'),
    path('confirmed_email/', views.confirmed_email, name='confirmed_email'),
    path('dev_team/', views.dev_team, name='dev_team'),
    path('changepass/', views.changePass, name='changepass'),
    path('accounts/', include('allauth.urls')),
    path('Globe/', include('Globe.urls')),

    # POST views
    path('view_status/', PostListView.as_view(), name='view_status'),
    path('view_status/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('view_status/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('view_status/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),

    # post search view
    path('search/', views.search, name='search'),

    # Update profile Views
    path('view_profile/', views.view_profile, name='view_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

    # email confirmation view
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    # password reset views
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='Globe/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='Globe/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='Globe/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='Globe/password_reset_complete.html'),
         name='password_reset_complete'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
