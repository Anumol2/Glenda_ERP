import requests
from django.db import models
from register_app.models import CustomUser
from django.core.exceptions import ValidationError
from decimal import Decimal  # For setting a default fallback value of zero


def validate_aadhar(value):
    if not value.isdigit() and not isinstance(value, str):
        raise ValidationError('Aadhar number must be numeric or a valid file.')


class EmployeeDetails(models.Model):
    employee_id = models.CharField(max_length=120, null=True, default="")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    joining_date = models.DateField(null=True)
    emergency_contact_name = models.CharField(max_length=100, null=True)
    emergency_contact_number = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], null=True)
    basic = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    aadhar_no = models.CharField(max_length=12, null=True, validators=[validate_aadhar])
    aadhar_file = models.FileField(upload_to='aadhar_files/', null=True, blank=True)
    street = models.CharField(max_length=150, null=True)
    pincode = models.CharField(max_length=9, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=120, null=True)
    designation = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(null=True)

    BloodGroupTypes = (
        ('AB+', 'AB+'),
        ('B+', 'B+'),
        ('A+', 'A+'),
        ('O+', 'O+'),
        ('AB-', 'AB-'),
        ('B-', 'B-'),
        ('A-', 'A-'),
        ('O-', 'O-'),
    )

    employee_blood_groups = models.CharField(max_length=100, choices=BloodGroupTypes, default='AB+')
    pf_no = models.CharField(max_length=22, unique=True, blank=True)
    employee_esi_no = models.CharField(max_length=17, unique=True, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    qualification_file = models.FileField(upload_to='qualification_files/', null=True, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    experience_file = models.FileField(upload_to='experience_files/', null=True, blank=True)

    def clean(self):
        # Custom validation to ensure at least one field is filled
        if not self.aadhar_no and not self.aadhar_file:
            raise ValidationError('You must provide either an Aadhar number or upload a file.')


class RequestLeave(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE, null=True)

    LEAVE_TYPE_CHOICES = (
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Paid Leave', 'Paid Leave'),
    )

    leave_type = models.CharField(max_length=100, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    reason = models.CharField(max_length=120, null=True)

    Approval_Type = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    approval_status = models.CharField(max_length=100, choices=Approval_Type, default='Pending')
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.approval_status}"


class Payroll(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)

    # Earnings
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    da = models.DecimalField(max_digits=10, decimal_places=2)
    ot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    leave_plus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))

    medical = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    insurance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    ta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    food_allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         default=Decimal('0.00'))

    # Deductions
    canteen_expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                          default=Decimal('0.00'))
    pf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    esi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))

    # Bonuses
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))

    # Computed field
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField()

    def __str__(self):
        return f"{self.employee}"