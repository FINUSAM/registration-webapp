from django import forms
from .models import Student
from django.core.exceptions import ValidationError

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['studentname', 'parentname', 'phonenumber', 'category']

    def clean_studentname(self):
        """Clean and convert student name to lowercase"""
        studentname = self.cleaned_data['studentname']
        # Strip spaces and convert to lowercase
        studentname = ' '.join(studentname.strip().split()).lower()
        return studentname

    def clean_parentname(self):
        """Clean and convert parent name to lowercase"""
        parentname = self.cleaned_data['parentname']
        # Strip spaces and convert to lowercase
        parentname = ' '.join(parentname.strip().split()).lower()
        return parentname

    def clean_phonenumber(self):
        """Clean and validate phone number"""
        phonenumber = self.cleaned_data['phonenumber']
        # Remove any spaces from phone number
        phonenumber = phonenumber.replace(" ", "")
        if len(phonenumber) != 10:
            raise ValidationError('Phone number must be exactly 10 digits.')
        if not phonenumber.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        return phonenumber

    def clean(self):
        """Override clean method to apply additional custom validations"""
        cleaned_data = super().clean()

        studentname = cleaned_data.get('studentname')
        parentname = cleaned_data.get('parentname')
        phonenumber = cleaned_data.get('phonenumber')
        category = cleaned_data.get('category')

        # Custom validation (example: if all fields are required)
        if not studentname or not parentname or not phonenumber or not category:
            raise ValidationError('All fields are required.')

        return cleaned_data
