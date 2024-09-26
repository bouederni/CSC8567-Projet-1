from django.http import JsonResponse
from public.models import Planet, Moon

def displayapi(request):
    planets = Planet.objects.all()
    data = list(planets.values("name", "diameter_km", "distance_from_sun_au", "orbital_period", "rotation_period", "moon_count", "planet_type", "has_ring_system", "picture"))

    return JsonResponse(data, safe=False)

# Create your views here.

