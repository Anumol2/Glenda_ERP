from django.db import models

from purchase_app.models import RawMaterials
from register_app.models import CustomUser


# Create your models here.


class vendor_register(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    vendor_phn=models.CharField(max_length=200,null=True)
    vendor_district=models.CharField(max_length=150,null=True)
    vendor_state=models.CharField(max_length=200,null=True)
    vendor_country=models.CharField(max_length=150,null=True)
    vendor_pincode=models.IntegerField(null=True)
    PAN_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    pan_yes_or_no = models.CharField(max_length=10, choices=PAN_CHOICES, default='yes', null=True)
    vendor_PANNBR=models.CharField(max_length=150,null=True,blank=True)
    vendor_Street=models.CharField(max_length=200,null=True)
    vendor_Landmark=models.CharField(max_length=200,null=True)
    vendor_Building=models.CharField(max_length=200,null=True)
    vendor_listofpdcts=models.CharField(max_length=150,null=True)
    materials = models.ManyToManyField(RawMaterials)
