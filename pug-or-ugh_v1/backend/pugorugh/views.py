from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView

from .models import Dog, UserDog, UserPref
from .serializers import (DogSerializer, UserDogSerializer,
                          UserPrefSerializer, UserSerializer)


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class ListCreateDog(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class RetrieveNextDogView(RetrieveAPIView):
    serializer_class = DogSerializer

    def get_queryset(self):
        user = self.request.user
        category = UserPref.objects.get(user=user)

        pref_dogs = Dog.objects.filter(
            gender__in=category.gender.split(','),
            size__in=category.size.split(','),
            age_classification__in=category.age.split(','),
            userdog__status=self.kwargs.get('type')[0].lower()
        )

        rel_type = self.kwargs.get('type')
        return pref_dogs

    def get_object(self):
        queryset = self.get_queryset()
        # pk is meant to be the dog.pk
        pk = self.kwargs.get('pk')  # -1
        dog = queryset.filter(id__gt=pk).first()

        if dog is None:
            if queryset.first() is None:
                raise Http404
            return queryset.first()
        return dog


class UpdateDogStatusView(UpdateAPIView):
    serializer_class = DogSerializer
    queryset = Dog.objects.all()

    def put(self, request, *args, **kwargs):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        userdog_queryset = UserDog.objects.filter(
            user=self.request.user,
            dog=dog,
            status=self.kwargs.get('type')[0].lower()
        )

        if userdog_queryset:
            save_dog = userdog_queryset.all()

            import pdb;
            pdb.set_trace()

        else:
            user_dog = UserDog.objects.create(
                user=self.request.user,
                dog=dog,
                status=self.kwargs.get('type')[0].lower()
            )

            serializer = DogSerializer(dog)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


   # def get_object(self):
    #    return UserDog.objects.filter(
   #         user__id=self.request.user.id,
   #         dog__id=self.kwargs.get('pk')
    #    ).first()

   # def put(self, request, pk, type):
    #    the_dog = self.get_object()
   #     the_dog.status = type[0].lower()
    #    the_dog.save()
   #     return Response(UserDogSerializer(the_dog).data)


class UserPrefUpdateView(APIView):
    serializer_class = UserPrefSerializer

    def get_object(self):
        return UserPref.objects.filter(user__id__exact=self.request.user.id).first()

    def get(self, request):
        user = self.get_object()
        serializer = UserPrefSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = self.get_object()
        serializer = UserPrefSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


