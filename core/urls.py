from django.urls import path
from .views import (
    SuperAdminListView,
    superadmin_register,
    superadmin_login,
    superadmin_create_building,
    superadmin_list_admins,
    admin_register,
    admin_login,
    admin_list_visitors,
    visitor_checking,
    visitor_verify_otp,
    visitor_select_room,
)

urlpatterns = [
    # SuperAdmin URLs
    path('superadmin/register/', superadmin_register, name='superadmin-register'),
    path('superadmin/login/', superadmin_login, name='superadmin-login'),
    path('superadmin/create_building/', superadmin_create_building, name='superadmin-create-building'),
    path('superadmin/list_admins/', superadmin_list_admins, name='superadmin-list-admins'),
    path('superadmins/', SuperAdminListView.as_view(), name='superadmin-list'),
    

    # Admin URLs
    path('admin/register/', admin_register, name='admin-register'),
    path('admin/login/', admin_login, name='admin-login'),
    path('admin/list_visitors/', admin_list_visitors, name='admin-list-visitors'),

    # Visitor URLs
    path('visitor/checking/', visitor_checking, name='visitor-checking'),
    path('visitor/verify_otp/', visitor_verify_otp, name='visitor-verify-otp'),
    path('visitor/select_room/', visitor_select_room, name='visitor-select-room'),
]
