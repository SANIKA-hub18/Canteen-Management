from django import forms
from qr.models import MenuImage
from .models import Employee

class MenuImageForm(forms.ModelForm):
    class Meta:
        model = MenuImage
        fields = ['image']
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'department']