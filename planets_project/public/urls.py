from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main_page, name="Main page"),
]
