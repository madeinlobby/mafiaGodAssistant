from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
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


@api_view(['POST'])
@permission_classes([AllowAny])
def post_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsOwnerOrAdmin])
def put_user(request, id):
    user = User.objects.get(id=id)
    serializer = UserSerializer(user, data=request)
    if serializer.is_valid:
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsOwnerOrAdmin])
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
