from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from MGA import GeneralFunctions
from MGA.models import User, Cafe
from MGA.serializers import CafeSerializer


@api_view(['POST', 'GET'])
def cafe_rating(request):
    score = request.data.get('score')
    if score > 5 or score < 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    cafe_id = request.data.get('cafe_id')
    cafe = User.objects.get(id=cafe_id)
    cafe.rate.mean_score = GeneralFunctions.make_mean(cafe.rate.mean_score, cafe.rate.number_of_votes, score)
    cafe.rate.number_of_votes += 1
    cafe.rate.save()
    cafe.save()
    return Response(status=status.HTTP_200_OK)


class CafeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer


@api_view(['POST'])
def create_cafe(request):
    serializer_context = {
        'request': request,
    }

    serializer = CafeSerializer(data=request.data, context=serializer_context)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
