from django.urls import path
from .views import RoomList, RoomJoin, Following, RoomDelete, AddBlacklist

urlpatterns = [
    path('', RoomList.as_view(), name='room'),
    path('join/', RoomJoin.as_view(), name='join'),
    path('delete/', RoomDelete.as_view(), name='delete'),
    path('following/', Following.as_view(), name='follow'),
    path("blacklist/add/", AddBlacklist.as_view(), name="add_black"),
]
