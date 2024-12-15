from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Student(models.Model):

    CATEGORY = [
        ("Anganvadi", "Anganvadi"),
        ("LKG", "LKG"),
        ("UKG", "UKG"),
        ("1st", "1st"),
        ("2nd", "2nd"),
        ("3rd", "3rd"),
        ("4th", "4th"),
        ("5th", "5th"),
        ("6th", "6th"),
        ("7th", "7th"),
    ]

    # Regex for validating 10-digit phone number
    phone_validator = RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')

    # Regex for validating student and parent names (only letters and spaces)
    name_validator = RegexValidator(r'^[a-zA-Z\s]+$', 'Enter a valid name. Only letters and spaces are allowed.')

    studentname = models.CharField(max_length=30, validators=[name_validator])
    parentname = models.CharField(max_length=30, validators=[name_validator])
    phonenumber = models.CharField(max_length=10, validators=[phone_validator])
    class_name = models.CharField(max_length=20, choices=CATEGORY)
    category = models.CharField(max_length=1)

    # Automatically set the creation timestamp when a record is created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Boolean field to indicate whether the student has paid
    paid = models.BooleanField(default=False)

    # Unique chest number for each student
    chestnumber = models.CharField(max_length=10, unique=True, help_text="Unique chest number for the student.")

    def clean(self):
        # Clean the studentname and parentname fields
        self.studentname = self.studentname.strip().lower()  # Convert to lowercase
        self.parentname = self.parentname.strip().lower()  # Convert to lowercase
        
        # Remove extra spaces between names
        self.studentname = ' '.join(self.studentname.split())
        self.parentname = ' '.join(self.parentname.split())

        # Clean phone number by removing spaces (if any)
        self.phonenumber = self.phonenumber.replace(" ", "")

        # Optional: You could add more validation logic here if needed.
        # For example, check that phone number is exactly 10 digits after cleaning.
        if len(self.phonenumber) != 10:
            raise ValidationError('Phone number must be exactly 10 digits.')

        super().clean()

    def generate_chestnumber(self):
        student_count = Student.objects.filter(category=self.category, paid=True).count() + 1
        new_chestnumber = f"{self.category}{str(student_count).zfill(3)}"
        return new_chestnumber

    def generate_unpaid_chestnumber(self):
        last_not_paid_student = Student.objects.filter(chestnumber__startswith="9").order_by('-chestnumber').first()

        if last_not_paid_student:
            last_number = int(last_not_paid_student.chestnumber)
            new_number = last_number + 1
        else:
            new_number = 1

        new_chestnumber = f"9{str(new_number).zfill(3)}"
        return new_chestnumber
    

    def save(self, *args, **kwargs):

        if self.class_name in ["Anganvadi", "LKG", "UKG"]:
            self.category = "1"
        elif self.class_name in ["1st", "2nd"]:
            self.category = "2"
        elif self.class_name in ["3th", "4th", "5th"]:
            self.category = "3"
        elif self.class_name in ["6th", "7th"]:
            self.category = "4"


        if not self.chestnumber:  # If the chest number is not already set
            if self.is_paid():
                self.chestnumber = self.generate_chestnumber()  # Generate the chest number
            else:
                self.chestnumber = self.generate_unpaid_chestnumber()
        elif self.chestnumber[0] == 'N' and self.is_paid():
            self.chestnumber = self.generate_chestnumber()

        self.full_clean()  # Ensure full validation (including cleaning)
        super().save(*args, **kwargs)


    def __str__(self):
        # Return a string representation for this student
        return f"{self.studentname} ({self.category}) - Chest No: {self.chestnumber} - Paid: {'Yes' if self.paid else 'No'}"

    # Method to check if the student has paid
    def is_paid(self):
        return self.paid

    class Meta:
        ordering = ['chestnumber']  # Order by chest number, ensuring registration order
        constraints = [
            models.UniqueConstraint(
                fields=['studentname', 'parentname', 'phonenumber', 'category'],
                name='unique_student_in_category_and_phone'
            ),
            # Adding a unique constraint for the chestnumber
            models.UniqueConstraint(
                fields=['chestnumber'],
                name='unique_chestnumber'
            )
        ]
