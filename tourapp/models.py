from django.db import models

class Destination(models.Model):
    place_name = models.CharField(max_length=100)
    weather = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    map_link = models.URLField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.place_name


class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destination_images/')

    def __str__(self):
        return f"Image for {self.destination.place_name}"
