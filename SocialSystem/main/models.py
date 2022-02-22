from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    organization = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    text = models.CharField(max_length=300)
    price = models.IntegerField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Points(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
