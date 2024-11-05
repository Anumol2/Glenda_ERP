

from django import forms

from purchase_app.models import RawMaterials
from vendor_app.models import vendor_register


class VendorRegisterForm(forms.ModelForm):
    materials = forms.ModelMultipleChoiceField(
        queryset=RawMaterials.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = vendor_register  # Ensure correct model name
        fields = [
            'vendor_phn',
            'vendor_district',
            'vendor_state',
            'vendor_country',
            'vendor_pincode',
            'pan_yes_or_no',
            'vendor_PANNBR',
            'vendor_Street',
            'vendor_Landmark',
            'materials',
            'vendor_Building'
        ]

        widgets = {
            'vendor_phn': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'vendor_district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
            'vendor_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'vendor_country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'vendor_pincode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'pan_yes_or_no': forms.Select(attrs={'class': 'form-control', 'placeholder': 'PAN'}),
            'vendor_PANNBR': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PAN Number'}),
            'vendor_Street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'vendor_Landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Landmark'}),
            'vendor_Building': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Landmark'}),

        }
