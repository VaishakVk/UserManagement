from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='user_home'),
    path('user/<user_id>/', views.get_permissions_user, name='get_user_permissions'),
    path('checkpermission/', views.check_user_permission, name='check_user_permission'),
    path('roles/<role_id>/', views.modify_role_permissions, name='modify_role_permissions'),
    path('permissions/<permission_id>/', views.delete_permissions, name='delete_permissions'),
    path('<page_not_found>/', views.error_404, name='error_404'),
]
