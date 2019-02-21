from .models import Dog, User
from .views import *

from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)


class ModelTest(APITestCase):
    def setUp(self):
        self.dog = Dog.objects.create(
            name='jack',
            image_filename='jack.jpg',
            breed='German',
            age=45,
            gender='Male',
            size='m'
        )
        self.user = User.objects.create(username='jack')
        self.factory = APIRequestFactory()

    def test_user_preference(self):
        view = set_user_preference
        request = self.factory.get('update-prefs')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'jack')

    def test_liked_dog(self):
        view = retrieve_next_dog
        request = self.factory.get('next-dog')
        force_authenticate(request)
        response = view(request, pk=self.dog.pk, type='liked')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(User.objects.count(), 1)

    def test_disliked_dog(self):
        view = retrieve_next_dog
        request = self.factory.get('next-dog')
        force_authenticate(request)
        response = view(request, pk=self.dog.pk, type='disliked')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(User.objects.count(), 1)
