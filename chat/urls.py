from django.urls import path
from .views import RoomList, RoomJoin, Following, RoomDelete, AddBlacklist, DeleteBlacklist, GroupChatJoin, GroupChatLeave

urlpatterns = [
    path('', RoomList.as_view(), name='room'),
    path('join/', RoomJoin.as_view(), name='join'),
    path('delete/', RoomDelete.as_view(), name='delete'),
    path('following/', Following.as_view(), name='follow'),
    path("blacklist/add/", AddBlacklist.as_view(), name="add_black"),
    path("blacklist/del/", DeleteBlacklist.as_view(), name="del_black"),
    path('studychatjoin/', GroupChatJoin.as_view(), name='sc_join'),
    path('studychatleave/', GroupChatLeave.as_view(), name='sc_leave'),
]
