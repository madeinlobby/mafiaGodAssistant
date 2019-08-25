from rest_framework import status
from rest_framework.response import Response

from chat.serializers import MessageSerializer


def create_message(request):
    serializer_context = {
        'request': request,
    }
    serializer = MessageSerializer(data=request.data, context=serializer_context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
