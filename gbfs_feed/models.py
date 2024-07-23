from django.db import models

# Create your models here.
class Station(models.Model):
  station_id = models.CharField(max_length=100, unique=True)
  name = models.CharField(max_length=200)
  latitude = models.DecimalField(max_digits=10, decimal_places=5)
  longitude = models.DecimalField(max_digits=10, decimal_places=5)
  capacity = models.IntegerField()

  def __str__(self):
        return self.name
  def get_coordinates(self):
      return (self.latitude, self.longitude)
  def get_formatted_coordinates(self):
      return f'Latitude: {self.latitude}, Longitude: {self.longitude}'
  def get_capacity(self):
      return self.capacity
  def to_dict(self):
        return {
            "station_id": self.station_id,
            "name": self.name,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "capacity": self.capacity
        }