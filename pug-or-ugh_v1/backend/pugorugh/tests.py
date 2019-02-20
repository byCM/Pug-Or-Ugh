from django.test import TestCase

from rest_framework.test import APITestCase
from .models import Dog

DOG1 = {
    'name': 'Jack',
    'image_filename': 'jack.jpg',
    'breed': 'German Sheppard',
    'age': '25',
    'gender': 'male',
    'size': 'm',
}
DOG2 = {
    'name': 'Eric',
    'image_filename': 'Eric.jpg',
    'breed': 'Corgi',
    'age': '40',
    'gender': 'male',
    'size': 's',
}


class ModelTest(APITestCase):
    def setUp(self):
        self.DOG1 = Dog.objects.create(**DOG1)
        self.DOG2 = Dog.objects.create(**DOG2)
        pass

