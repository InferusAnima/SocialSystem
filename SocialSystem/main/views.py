from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Task, User
from .forms import CreateNewList
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


def home(response):
    return render(response, "main/home.html", {})


@login_required(login_url='login')
def tasks(response):
    tasks = list(Task.objects.all())
    User.objects.get(id=response.user.id)
    org = response.user.groups.all()[0].name == 'organization'
    return render(response, "main/tasks.html", {"tasks": tasks, 'org': org})


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
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST, response.FILES)

        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            beginning = form.cleaned_data["beginning"]
            geocode = form.cleaned_data["geocode"]
            image = form.cleaned_data["image"]
            limit = form.cleaned_data["limit"]
            award = form.cleaned_data["award"]
            t = Task(organization=response.user, name=name, award=award, description=description,
                     beginning=beginning, geocode=geocode, limiter=limit, photo=image)
            t.save()
            response.user.task.add(t)

            return HttpResponseRedirect(f"/tasks/{t.id}")

    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form": form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['organization'])
def control(response, id):
    tasks = list(filter(lambda x: x.user and x.organization.id == id, Task.objects.all()))
    return render(response, "main/control.html", {"tasks": tasks})


@login_required(login_url='login')
def user_info(response, id):
    user = User.objects.get(id=id)
    return render(response, "main/user_info.html", {"c_user": user})
