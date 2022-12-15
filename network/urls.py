
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posting", views.posting, name="posting"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like_handler", views.like_handler, name="like_handler"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow_handler", views.follow_handler, name="follow_handler")
]
