from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from django.utils import timezone




# Create your views here.

def home(request):
    return render(request, 'home.html')


def students(request):
    # Get all students
    students = Student.objects.all()

    # Separate students by payment status
    paid_students = []
    unpaid_students = []

    # Group students by category (excluding unpaid students from their original categories)
    categorized_students = {}

    for student in students:
        if student.paid:
            if student.category not in categorized_students:
                categorized_students[student.category] = []
            categorized_students[student.category].append(student)
        else:
            unpaid_students.append(student)

    # Add unpaid students as a separate category at the end
    return render(request, 'students.html', {
        'categorized_students': categorized_students,
        'unpaid_students': unpaid_students  # Separate context for "Not Paid"
    })


def student(request, chestnumber):
    student = get_object_or_404(Student, chestnumber=chestnumber)
    return render(request, 'student.html', {'student': student})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            new_student = form.save()  # Save the form to create the student
            chestnumber = new_student.chestnumber  # Get the chestnumber of the new student
            request.session['chestnumber'] = chestnumber
            return redirect('payment')
        else:
            student_data = form.cleaned_data
            try:
                student = Student.objects.get(
                    studentname=student_data['studentname'], 
                    parentname=student_data['parentname'], 
                    phonenumber=student_data['phonenumber'], 
                    category=student_data['category']
                )
                request.session['chestnumber'] = student.chestnumber
                return redirect('payment')
            except Student.DoesNotExist:
                form.add_error(None, "Invalid")
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})


def redirect_to_payment(request, chestnumber):
    request.session['chestnumber'] = chestnumber
    return redirect('payment')

def payment(request):
    chestnumber = request.session.get('chestnumber')

    if chestnumber is None:
        return redirect('register')

    student = get_object_or_404(Student, chestnumber=chestnumber)

    if request.method == 'POST':

        payment_status = request.POST.get('payment_status')  # E.g., success, failure, etc.
        del request.session['chestnumber']
        
        if payment_status == 'success':
            student.paid = True
            student.chestnumber = student.generate_chestnumber()
            student.save()
            messages.success(request, "Payment was successful! Your account is now marked as paid.")
            return redirect('student', chestnumber=student.chestnumber)
        else:
            messages.error(request, "Payment failed. Please try again or contact support.")
            return redirect('student', chestnumber=student.chestnumber)
    
    # If the request method is GET, render the payment page
    return render(request, 'payment.html', {'student': student})

import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def download(request):
    # Query all student records
    queryset = Student.objects.all().values('studentname', 'parentname', 'phonenumber', 'category', 'class_name', 'created_at', 'paid', 'chestnumber')

    # Convert the queryset to a DataFrame
    df = pd.DataFrame(queryset)

    # Ensure 'created_at' is timezone-unaware before exporting
    if 'created_at' in df.columns:
        # Remove timezone info and make datetime naive (timezone-unaware)
        df['created_at'] = df['created_at'].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) else None)

    # Create a HttpResponse to serve the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=students_data.xlsx'

    # Write the DataFrame to the response using Pandas Excel writer
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')

    return response
