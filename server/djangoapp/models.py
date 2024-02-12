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
    year = models.DateField(null=True)

    def __str__(self):
        return f"Name: {self.name}, Type: {self.car_type}, Year: {self.year}, Make: {self.car_make}"

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip, state):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
        self.state = state

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    
    def __init__(self, id, name, purchase, review, dealership, sentiment):
        self.id = id
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = None
        self.dealership = dealership
        self.car_make = None
        self.car_model = None
        self.car_year = None
        self.sentiment = sentiment

    def __str__(self):
        return f"{self.name}, wrote '{self.review}'. Which is a {self.sentiment} review"

    