from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from MGA import GeneralFunctions
from MGA.models import User
from MGA.permissions import IsOwnerOrAdmin
from MGA.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# TODO Question
"""
 1.mishe id ro kolan hazf kard ba resquest.POST['id'] bedast avord?
 2.return ha injori bashe okeye? 
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    user = User.objects.get(id=id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@permission_classes([AllowAny])
def post_user(request):
    serializer_context = {
        'request': request,
    }

    serializer = UserSerializer(data=request.data, context=serializer_context)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsOwnerOrAdmin])
def put_user(request, id):
    serializer_context = {
        'request': request,
    }
    user = User.objects.get(id=id)
    serializer = UserSerializer(user, data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsOwnerOrAdmin])
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST', 'GET'])
def user_rating(request):  # az panj bede
    score = request.data.get('score')
    if score > 5 or score < 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user_id = request.data.get('user_id')
    user = User.objects.get(id=user_id)
    user.rate.mean_score = GeneralFunctions.make_mean(user.rate.mean_score, user.rate.number_of_votes, score)
    user.rate.number_of_votes += 1
    user.rate.save()
    user.save()
    return Response(status=status.HTTP_200_OK)


