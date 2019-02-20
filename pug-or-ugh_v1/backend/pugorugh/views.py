from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .models import Dog, UserDog, UserPref
from .serializers import (DogSerializer, UserDogSerializer,
                          UserPrefSerializer, UserSerializer)


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


@api_view(['PUT'])
def update_dog(request, pk, type):
    """Updates dogs status"""
    user = request.user
    dog = Dog.objects.get(id=pk)

    userdog = UserDog.objects.get(user=user, dog=dog)
    userdog.status = type[0].lower()
    userdog.save()

    serializer = DogSerializer(dog)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view()
def retrieve_next_dog(request, pk, type):
    """Retrieves next dog, displays dogs based on users preferences"""
    category = UserPref.objects.get(user=request.user)
    dogs = Dog.objects.filter(
        pk__gt=pk,
        gender__in=category.gender.split(','),
        size__in=category.size.split(','),
        age_classification__in=category.age.split(','),
        userdog__status=type[0].lower(),
        userdog__user=request.user,
    )
    dog = dogs.first()
    if not Dog:
        return Response(data={'error': "No dog found!"},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = DogSerializer(dog)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

