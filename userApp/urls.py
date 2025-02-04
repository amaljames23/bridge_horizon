from django.urls import path
from . import views

urlpatterns = [
    path('user_home',views.user_home,name='user_home'),
    path('user_reg',views.user_reg,name='user_reg'),
    path('user_view_nots',views.user_view_nots,name='user_view_nots'),
    path('user_send_complaints',views.user_send_complaints,name='user_send_complaints'),
    path('user_view_theaters',views.user_view_theaters,name='user_view_theaters'),
]