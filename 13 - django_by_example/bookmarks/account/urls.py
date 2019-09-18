from django.urls import path
from django.contrib.auth import views as auth_views

from .import views

urlpatterns = [
    # path('login/',views.user_login,name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

    path('users/', views.user_list, name='user_list'),

    path('users/follow/', views.user_follow, name='user_follow'), # 该路由必须要先于 user_detail 路由，否则会被 user_detail 路由覆盖
    
    path('users/<username>/', views.user_detail, name='user_detail'),
]
