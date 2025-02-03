from django.urls import path
from . import views

urlpatterns = [

    path('',views.home,name='home'),
    path('login',views.login_form,name='login'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('admin_manage_users',views.admin_manage_users,name='admin_manage_users'),
    path('delete_user/<aid>',views.delete_user,name='delete_user'),
    path('admin_view_compalints',views.admin_view_compalints,name='admin_view_compalints'),
    path('admin_send_reply/<cid>',views.admin_send_reply,name='admin_send_reply'),
    path('admin_manage_films',views.admin_manage_films,name='admin_manage_films'),
    path('admin_delete_films/<id>',views.admin_delete_films,name='admin_delete_films'),
    path('admin_update_films/<id>',views.admin_update_films,name='admin_update_films'),
    path('admin_view_Review',views.admin_view_Review,name='admin_view_Review'),
]