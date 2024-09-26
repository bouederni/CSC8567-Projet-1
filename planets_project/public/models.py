from django.db import models

class Planet(models.Model):
    PLANET_TYPE_CHOICES = [
        ('terrestrial', 'Terrestrial'),
        ('gas_giant', 'Gas Giant'),
        ('ice_giant', 'Ice Giant'),
        ('dwarf', 'Dwarf Planet'),
    ]

    name = models.CharField(max_length=50, unique=True)
    diameter_km = models.FloatField(help_text="Diameter in kilometers")
    distance_from_sun_au = models.FloatField(help_text="Average distance from the Sun in Astronomical Units (AU)")
    orbital_period = models.FloatField(help_text="Orbital period in Earth days")
    rotation_period = models.FloatField(help_text="Rotation period in Earth days")
    moon_count = models.IntegerField(default=0)
    planet_type = models.CharField(max_length=20, choices=PLANET_TYPE_CHOICES)
    has_ring_system = models.BooleanField(default=False)
    picture = models.URLField(max_length=100, default="")

    def __str__(self):
        return self.name   

class Moon(models.Model):
    name = models.CharField(max_length=50)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='moons')
    diameter_km = models.FloatField(help_text="Diameter in kilometers")
    orbital_period_days = models.FloatField(help_text="Orbital period in Earth days")

    def __str__(self):
        return f"{self.name} (Moon of {self.planet.name})"  