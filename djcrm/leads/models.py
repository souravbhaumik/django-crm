from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class Lead(models.Model):
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE)
    SOURCE_CHOICES = (
        ('YouTube', 'YouTube'),
        ('Google', 'Google'),
        ('Newsletter', 'Newsletter'),
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=25)

    # phoned = models.BooleanField(default=False)
    # source = models.CharField(choices=SOURCE_CHOICES,
    #                           max_length=100, default='YouTube')

    # profile_picture = models.ImageField(blank=True, null=True)
    # special_filters = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + "|" + " " + str(self.last_name)


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
