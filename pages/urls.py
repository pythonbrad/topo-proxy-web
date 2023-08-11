from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("ping/", views.ping, name="ping"),
    path("my-config/", views.get_config, name="my-config"),
    path("new-config/", views.new_config, name="new-config"),
    path("drop-config/<int:pk>", views.drop_config, name="drop-config"),
    path("reload-config/<int:pk>", views.reload_config, name="reload-config"),
]
