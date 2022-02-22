from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from main.models import Points


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            points = Points(user=user, points=0)
            points.save()
            login(response, user)
        else:
            return render(response, "register/register.html", {"form": form})

        return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})
