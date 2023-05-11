from rest_framework.viewsets import ModelViewSet
from gametrail.models import *
from gametrail.api.serializers import *
from gametrail.api.Chat.chatSerializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ChatByTrailId(ModelViewSet):
    http_method_names = ['get']
    def get_queryset(self):
        chatQuerySet = ChatTrail.objects.filter(trail_id = self.request.data["trailId"])
        chatQuerySet = chatQuerySet.order_by('-creationDate')[:50]
        return chatQuerySet

    serializer_class = ChatByTrailIdSerializer

class PostChatAPIViewSet(APIView):
    http_method_names = ['post']

    def post(self, request, format=None):
        trailId = request.data['trailId']
        text = request.data['text']
        creationDate = datetime.now()
        userId = request.data["userId"]
        
        trail = Trail.objects.get(pk = trailId)
        
        is_user_valid = False
        allUserInTrail = UserInTrail.objects.filter(trail_id = trailId)
        for user in allUserInTrail:
            if (user.user.username == request.user.username) & (request.user.username == User.objects.get(pk = userId).username):
                is_user_valid = True
        
        if (not is_user_valid):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif (is_user_valid):
            user = User.objects.get(pk = userId)
            chatTrail = ChatTrail.objects.create(
                text = text, creationDate = creationDate, user = user, trail = trail
            )
            chatTrail.save()

            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)