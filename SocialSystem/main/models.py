from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


def user_directory_path(instance, filename):
    return 'users/{0}'.format(filename)


def task_directory_path(instance, filename):
    return 'tasks/{0}'.format(filename)


class Task(models.Model):
    organization = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task", null=True)
    user = models.ManyToManyField(User, related_name="user", null=True, blank=True)
    name = models.CharField(max_length=128)
    beginning = models.DateTimeField(default=timezone.now, null=True)
    photo = models.ImageField(upload_to=user_directory_path, null=True)
    geocode = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    award = models.IntegerField(default=0)
    limiter = models.IntegerField(default=1)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class Benefit(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    cost = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, blank=True)
    location = models.CharField(max_length=30, blank=True)
    points = models.IntegerField(default=0)
    about = models.CharField(max_length=256, blank=True)
    photo = models.ImageField(upload_to=task_directory_path, verbose_name="Фото", null=True)
    benefits = models.ManyToManyField(Benefit, related_name="benefit", null=True, blank=True)
