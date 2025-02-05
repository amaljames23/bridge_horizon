from django.urls import path
from . import views

urlpatterns = [
    path('user_home',views.user_home,name='user_home'),
    path('user_reg',views.user_reg,name='user_reg'),
    path('user_view_nots',views.user_view_nots,name='user_view_nots'),
    path('user_send_complaints',views.user_send_complaints,name='user_send_complaints'),
    path('user_view_theaters',views.user_view_theaters,name='user_view_theaters'),
    path('user_book_seats/<theater_id>/<screening_slot_id>',views.user_book_seats,name='user_book_seats'),
    path('user_seat_confirm/', views.user_seat_confirm, name='user_seat_confirm'),
    ################
    path('filmaker_reg', views.filmaker_reg, name='filmaker_reg'),
    path('filmaker_home/', views.filmaker_home, name='filmaker_home'),
    path('filmmaker_view_prof', views.filmmaker_view_prof, name='filmmaker_view_prof'),
    path('film_maker_view_theaters', views.film_maker_view_theaters, name='film_maker_view_theaters'),
    path('film_maker_book_seats/<theater_id>/<screening_slot_id>',views.film_maker_book_seats,name='film_maker_book_seats'),
    path('film_maker_seat_confirm/', views.film_maker_seat_confirm, name='film_maker_seat_confirm'),

]