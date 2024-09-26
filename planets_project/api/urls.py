from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.displayapi, name="API"),
]
