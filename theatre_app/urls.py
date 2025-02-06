from django.urls import path
from . import views

urlpatterns = [

    path('theatre_home',views.theatre_home,name='theatre_home'),
    path('thearte_registration',views.theatre_registration,name='thearte_registration'),
    path('theatre_owner_registration',views.theatre_owner_registration,name='theatre_owner_registration'),
    path('theatre_view_profile',views.theatre_view_profile,name='theatre_view_profile'),
    path('thearter_owner_update_profile/<lid>',views.thearter_owner_update_profile,name='thearter_owner_update_profile'),
    path('theatre_view_others_theartes',views.theatre_view_others_theartes,name='theatre_view_others_theartes'),
    path('theatre_manage_seats/<id>',views.theatre_manage_seats,name='theatre_manage_seats'),
    path('theatre_manage_slots/<id>',views.theatre_manage_slots,name='theatre_manage_slots'),
    path('theatre_update_slots/<id>',views.theatre_update_slots,name='theatre_update_slots'),
    path('theatre_delete_slots/<id>',views.theatre_delete_slots,name='theatre_delete_slots'),
    path('thearte_view_booking/<id>',views.thearte_view_booking,name='thearte_view_booking'),
    path('theatre_view_payment_details/<id>',views.theatre_view_payment_details,name='theatre_view_payment_details'),
    path('theatre_view_producers',views.theatre_view_producers,name='theatre_view_producers'),
    path('theatre_chat/<id>',views.theatre_chat,name='theatre_chat'),
    path('theatre_view_producermsg',views.theatre_view_producermsg,name='theatre_view_producermsg'),
     path('theatre_insert_theatrechat/<msg>',views.theatre_insert_theatrechat,name='theatre_insert_theatrechat'),

]