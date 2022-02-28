from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("tasks/<int:id>", views.task, name="task"),
    path("tasks/", views.tasks, name="tasks"),
    path("control/<int:id>", views.control, name="control"),
    path("user_info/<int:id>", views.user_info, name="user_info"),
]
