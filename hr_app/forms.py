from django import forms
from .models import EmployeeDetails,RequestLeave,Payroll

class EmployeeDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ['emergency_contact_number','aadhar_no','street','pincode','state','country','landmark','district','basic','date_of_birth','aadhar_file','employee_blood_groups','pf_no','employee_esi_no','qualification','qualification_file','experience','experience_file']
        widgets = {
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhar_no': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode':forms.TextInput(attrs={'class': 'form-control'}),
            'state':forms.TextInput(attrs={'class': 'form-control'}),
            'country':forms.TextInput(attrs={'class': 'form-control'}),
            'landmark':forms.TextInput(attrs={'class': 'form-control'}),
            'district':forms.TextInput(attrs={'class': 'form-control'}),
            'basic':forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'aadhar_file':forms.FileInput(attrs={'class': 'form-control'}),
            'employee_blood_groups':forms.Select(attrs={'class': 'form-control'}),
            'pf_no':forms.TextInput(attrs={'class': 'form-control'}),
            'employee_esi_no':forms.TextInput(attrs={'class': 'form-control'}),
            'qualification':forms.TextInput(attrs={'class': 'form-control'}),
            'qualification_file':forms.FileInput(attrs={'class': 'form-control'}),
            'experience':forms.TextInput(attrs={'class': 'form-control'}),
            'experience_file':forms.FileInput(attrs={'class': 'form-control'}),
        }

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = RequestLeave
        fields = ['leave_type','start_date','end_date','reason',]
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [ 'hra', 'da', 'ot', 'leave_plus', 'medical', 'insurance', 'ta', 'food_allowance', 'canteen_expense', 'pf', 'esi', 'bonuses', 'pay_date']
        widgets = {
            'hra': forms.TextInput(attrs={'class': 'form-control'}),
            'da': forms.TextInput(attrs={'class': 'form-control'}),
            'ot': forms.TextInput(attrs={'class': 'form-control'}),
            'leave_plus': forms.TextInput(attrs={'class': 'form-control'}),
            'medical': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance': forms.TextInput(attrs={'class': 'form-control'}),
            'ta': forms.TextInput(attrs={'class': 'form-control'}),
            'food_allowance': forms.TextInput(attrs={'class': 'form-control'}),
            'canteen_expense': forms.TextInput(attrs={'class': 'form-control'}),
            'pf': forms.TextInput(attrs={'class': 'form-control'}),
            'esi': forms.TextInput(attrs={'class': 'form-control'}),
            'bonuses': forms.TextInput(attrs={'class': 'form-control'}),
            'pay_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }