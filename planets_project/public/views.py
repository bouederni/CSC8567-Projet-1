from django.shortcuts import render
from .models import Planet

def main_page(request):
    planets = Planet.objects.all()
    return render(request, 'mainpage.html', {'planets': planets})
