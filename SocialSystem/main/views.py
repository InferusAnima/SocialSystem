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
    org = response.user.groups.all()[0].name == 'organization'
    return render(response, "main/tasks.html", {"tasks": tasks, 'org': org})


@login_required(login_url='login')
def task(response, id):
    task = Task.objects.get(id=id)
    org = response.user.groups.all()[0].name == 'organization'
    can_take = response.user.id not in [i.id for i in task.user.all()] and len(list(task.user.all())) <= task.limiter and not task.complete
    if response.method == "POST":
        if response.POST.get("take"):
            task.user.add(response.POST.get("take"))  # set
            task.save()
        elif response.POST.get("kick"):
            task.user.remove(response.POST.get("kick"))
        elif response.POST.get("complete"):
            task.complete = True
            task.save()
            for person in task.user.all():
                person.profile.points += task.award
                person.profile.save()
            task.delete()
            return redirect('/tasks')
        return redirect(f'/tasks/{id}')
    return render(response, "main/task.html", {"task": task, "org": org, "can_take": can_take})


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
def user_info(response, id):
    user = User.objects.get(id=id)
    return render(response, "main/user_info.html", {"c_user": user})
