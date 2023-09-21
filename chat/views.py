from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from .models import Room, Message
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer, BlacklistSerializer
from user.models import Follower, Blacklist

User = get_user_model()


class RoomList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        rooms = Room.objects.filter(Q(firstuser=user) | Q(
            seconduser=user), is_active=True).values()

        room_list = []

        for room in rooms:
            info = {}
            message = Message.objects.filter(
                room=room['id']).order_by('-created_at').values()
            try:
                message[0]
            except:
                info['recent'] = {'content': '첫 메시지를 보내보세요.'}
            else:
                info['recent'] = message[0]

            if user.id == room['firstuser_id']:
                target = User.objects.get(pk=room['seconduser_id'])
            elif user.id == room['seconduser_id']:
                target = User.objects.get(pk=room['firstuser_id'])

            serializer = UserSerializer(target)
            info['room'] = room
            info['target'] = serializer.data

            room_list.append(info)

        datas = {
            "rooms": room_list
        }
        return Response(datas, status=status.HTTP_200_OK)


class RoomJoin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        target = User.objects.get(pk=request.data['target'])
        rooms = Room.objects.filter(Q(firstuser=user, seconduser=target) | Q(
            firstuser=target, seconduser=user), is_active=True)

        if not rooms:
            room = Room.objects.create(firstuser=user, seconduser=target)
            room.title = f'room{room.pk}'
            room.save()
            datas = {
                "message": "채팅방 생성 성공",
            }
            return Response(datas, status=status.HTTP_200_OK)
        else:
            datas = {
                "message": "채팅방이 이미 존재합니다.",
            }
            return Response(datas, status=status.HTTP_200_OK)


class RoomDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            room = Room.objects.get(pk=request.data['target'], is_active=True)
        except:
            datas = {
                "message": "이미 삭제된 채팅방 입니다.",
            }
            return Response(datas, status=status.HTTP_200_OK)

        room.is_active = False
        room.save()
        datas = {
            "message": "채팅방이 삭제 되었습니다..",
        }
        return Response(datas, status=status.HTTP_200_OK)


class Following(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        my_blacklist = Blacklist.objects.get_or_create(user=user)
        blacklist = my_blacklist[0].blacklist['blacklist']

        followings = Follower.objects.filter(follower_id=request.user)
        newFollowings = []
        for following in followings:
            if not following.target_id.id in blacklist:
                user_blacklist = Blacklist.objects.get_or_create(
                    user=following.target_id)[0]
                u_blacklist = user_blacklist.blacklist['blacklist']
                if not user.id in u_blacklist:
                    following_pf = UserSerializer(following.target_id).data
                    newFollowings.append(following_pf)

        response = {"following": newFollowings,
                    "blacklist": BlacklistSerializer(my_blacklist[0]).data}

        return Response(data=response, status=status.HTTP_200_OK)


class AddBlacklist(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user_blacklist = Blacklist.objects.filter(user=user)[0]

        room = Room.objects.get(pk=request.data['target'], is_active=True)
        room.is_active = False
        room.save()

        if user.id == room.firstuser_id:
            target = room.seconduser_id
        elif user.id == room.seconduser_id:
            target = room.firstuser_id

        add_blacklist = user_blacklist.blacklist['blacklist']
        if not target in add_blacklist:
            add_blacklist.append(target)
            add_blacklistProfile = user_blacklist.blacklist['blacklist_profile']
            target_user = User.objects.get(id=target)
            target_serializer = UserSerializer(target_user)
            add_blacklistProfile.append(target_serializer.data)
            user_blacklist.save()
            datas = {
                'message': '해당 유저를 차단하였습니다.'
            }

            return Response(data=datas, status=status.HTTP_200_OK)

        datas = {
            'message': '이미 차단한 유저입니다.'
        }
        return Response(data=datas, status=status.HTTP_200_OK)


class DeleteBlacklist(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        blacklist = Blacklist.objects.get(user=user)
        target = int(request.data['target'])
        user_blacklist = blacklist.blacklist['blacklist']
        if target in user_blacklist:
            user_blacklistProfile = blacklist.blacklist['blacklist_profile']
            idx = user_blacklist.index(target)
            user_blacklist.pop(idx)
            profile_idx = next((index for (index, item) in enumerate(
                user_blacklistProfile) if item['id'] == str(target)), None)

            user_blacklistProfile.pop(profile_idx)
            blacklist.save()

            datas = {
                'message': '차단이 해제되었습니다.'
            }
            return Response(data=datas, status=status.HTTP_200_OK)

        datas = {
            'message': '이미 해제된 유저입니다.'
        }
        return Response(data=datas, status=status.HTTP_200_OK)
