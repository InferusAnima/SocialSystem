from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from main.models import Points


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save()
            points = Points(user=user, points=0)
            points.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            login(response, user)
        else:
            return render(response, "register/register.html", {"form": form})

        return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})
