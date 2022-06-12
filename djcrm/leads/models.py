from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey('UserProfile', models.CASCADE)

    def full_name(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, null=True, blank=True)
    organisation = models.ForeignKey('UserProfile', models.CASCADE, null=True, blank=True)
    SOURCE_CHOICES = (
        ('YouTube', 'YouTube'),
        ('Google', 'Google'),
        ('Newsletter', 'Newsletter'),
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=25)

    def full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def __str__(self):
        return self.first_name + " " + "|" + " " + str(self.last_name) + " " + "|" + "Age:" + str(self.age)


def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created, sender)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
