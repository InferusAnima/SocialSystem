from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Task
from .forms import CreateNewList
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required


def home(response):
    return render(response, "main/home.html", {})


@login_required(login_url='login')
def tasks(response):
    tasks = list(filter(lambda x: not x.user, Task.objects.all()))
    return render(response, "main/tasks.html", {"tasks": tasks})


@login_required(login_url='login')
def task(response, id):
    ls = Task.objects.get(id=id)
    if not ls.user and response.user != ls.organization:
        if response.method == "POST":
            if response.POST.get("take"):
                ls.user = response.user
                ls.save()
            return redirect(f'/tasks/{id}')

        return render(response, "main/task.html", {"ls": ls, "taken": False, "org": False})
    elif ls.user and response.user == ls.organization:
        if response.method == "POST":
            if response.POST.get("revoke"):
                ls.user = None
                ls.save()
            elif response.POST.get("complete"):
                ls.complete = True
                ls.user.points.points += ls.price
                ls.user.points.save()
                ls.save()
            elif response.POST.get("uncomplete"):
                ls.complete = False
                ls.user.points.points -= ls.price
                ls.user.points.save()
                ls.save()
            return redirect(f'/tasks/{id}')

        return render(response, "main/task.html", {"ls": ls, "taken": True, "org": True})
    elif response.user == ls.organization:
        return render(response, "main/task.html", {"ls": ls, "taken": False, "org": True})
    else:
        return render(response, "main/task.html", {"ls": ls, "taken": True, "org": False})


@login_required(login_url='login')
@allowed_users(allowed_roles=['organization'])
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            text = form.cleaned_data["text"]
            price = form.cleaned_data["price"]
            t = Task(text=text, price=price)
            t.save()
            response.user.task.add(t)

            return HttpResponseRedirect(f"/tasks/{t.id}")

    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form": form})
