from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, default='u')
    age = models.IntegerField()
    age_classification = models.CharField(max_length=255, default='u')
    gender = models.CharField(max_length=1,
                              choices=[('m', 'Male'),
                                       ('f', 'Female'),
                                       ('u', 'Unknown')]
                              )
    size = models.CharField(max_length=2,
                            choices=[('s', 'Small'),
                                     ('m', 'Medium'),
                                     ('l', 'Large'),
                                     ('xl', 'Extra Large'),
                                     ('u', 'Unknown')]
                            )

    def save(self, *args, **kwargs):
        if self.age < 12:
            self.age_classification = 'b'
        elif self.age <= 24:
            self.age_classification = 'y'
        elif self.age <= 72:
            self.age_classification = 'a'
        else:
            self.age_classification = 's'
        super(Dog, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1,
                              choices=[('l', 'Liked'),
                                       ('d', 'Disliked'),
                                       ('u', 'Undecided')],
                              )


class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=255, default='b,y,a,s')
    gender = models.CharField(max_length=255, default='m,f')
    size = models.CharField(max_length=255, default='s,m,l,xl')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
      UserPref.objects.create(user=instance)

      dogs = Dog.objects.all()

      for dog in dogs:
          UserDog.objects.create(
              user=instance,
              dog=dog,
<<<<<<< HEAD
              status='u'
=======
              status='u',
>>>>>>> 7eb7d2ca0d8d39f682a3c9eef00bf89a28b0f058
          )
