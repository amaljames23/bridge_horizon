from django.urls import path
from . import views

urlpatterns = [

    path('',views.home,name='home'),
    path('login',views.login_form,name='login'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('admin_manage_users',views.admin_manage_users,name='admin_manage_users'),
    path('accept_user/<aid>',views.accept_user,name='accept_user'),
    path('reject_user/<aid>',views.reject_user,name='reject_user'),
    path('admin_view_compalints',views.admin_view_compalints,name='admin_view_compalints'),
    path('admin_send_reply/<cid>',views.admin_send_reply,name='admin_send_reply'),
    path('admin_manage_films',views.admin_manage_films,name='admin_manage_films'),
    path('admin_delete_films/<id>',views.admin_delete_films,name='admin_delete_films'),
    path('admin_update_films/<id>',views.admin_update_films,name='admin_update_films'),
    path('admin_view_Review',views.admin_view_Review,name='admin_view_Review'),
    path('admin_send_notification',views.admin_send_notification,name='admin_send_notification'),
    path('admin_view_producers',views.admin_view_producers,name='admin_view_producers'),
    path('admin_view_theaters',views.admin_view_theaters,name='admin_view_theaters'),
    path('accept_theaterowner/<lid>',views.accept_theaterowner,name='accept_theaterowner'),
    path('reject_theaterowner/<lid>',views.reject_theaterowner,name='reject_theaterowner'),

    path('admin_view_ContentManager',views.admin_view_ContentManager,name='admin_view_ContentManager'),
    path('accept_content_manager/<lid>',views.accept_content_manager,name='accept_content_manager'),
    path('reject_content_manager/<lid>',views.reject_content_manager,name='reject_content_manager'),


]