from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=300, default="No description available")

    def __str__(self):
        return f"Make: {self.name}, Description: {self.description}"


class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    HATCH = 'Hatch'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (HATCH, 'Hatch')
    ]
    car_make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(null=False, max_length=30)
    car_type = models.CharField(max_length=20, choices=CAR_TYPES, default=SEDAN)
    year = models.DateField(now)

    def __str__(self):
        return f"Name: {self.name}, Type: {self.car_type}, Year: {self.year}, Make: {self.car_make}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
