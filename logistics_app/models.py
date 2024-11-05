from django.db import models
from django.forms import ValidationError
from production_app.models import water_Finished_Goods
from register_app.models import CustomUser


class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=200, null=True)
    vehicle_nbr = models.CharField(max_length=200, null=True)
    vehicle_img = models.ImageField(upload_to='images/', null=True)
    vehicle_insurance_date = models.DateField(null=True)
    vehicle_taxes_date = models.DateField(null=True)
    vehicle_fasttag = models.IntegerField(null=True)
    vehicle_pollution_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.vehicle_name} ({self.vehicle_nbr})"


import requests

class Route(models.Model):
    route_name = models.CharField(max_length=200, null=True)
    starting_point = models.CharField(max_length=200, null=True)
    ending_point = models.CharField(max_length=200, null=True)
    total_distance = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.route_name

class Route_Plan(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE,null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE,default=True)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE,default=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.route} - {self.driver} on {self.date} at {self.time}"



from django.core.exceptions import ValidationError
from django.utils import timezone

class Driver(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    license_number = models.CharField(max_length=200, null=True)
    aadhaar_number = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    license_exp_date = models.DateField(null=True)
    upload_license = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.driver_name

    def formatted_license_exp_date(self):
        if self.license_exp_date and self.license_exp_date >= timezone.now().date():
            return self.license_exp_date.strftime('%d-%m-%Y')
        return None  # Return None if the date is in the past

    def clean(self):
        if self.license_exp_date and self.license_exp_date < timezone.now().date():
            raise ValidationError("License expiration date cannot be in the past.")


class logistics_report(models.Model):
    date = models.DateField(null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    stock = models.ForeignKey(water_Finished_Goods, on_delete=models.CASCADE, null=True )

class Vehicle_Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    CHOICES = (
        ('Fuel ', 'Fuel'),
        ('FastTag', 'FastTag'),
        ('Tyre', 'Tyre'),
        ('Oil', 'Oil'),
        ('Insurance', 'Insurance'),
        ('Pollution', 'Pollution'),
        ('Tax', 'Tax'),
        ('CommonRepair', 'CommonRepair'),

    )
    TypeofMaintenance = models.CharField(max_length=20, choices=CHOICES,null=True)
    amount = models.FloatField(default=0.0,null=True,blank=False)
    Remarks = models.CharField(max_length=250,null=True)

    def clean(self):
        if self.amount < 0:
            raise ValidationError('Amount must be a positive float.')