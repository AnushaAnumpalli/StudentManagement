from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
from .forms import StudentForm

# ---------------- AUTH VIEWS ----------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "✅ Login successful!")
            return redirect('home')
        else:
            messages.error(request, "❌ Invalid credentials")
            return render(request, 'students/login.html')
    return render(request, 'students/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, "👋 You have been logged out.")
    return redirect('login')

# ---------------- DASHBOARD ----------------
@login_required
def home(request):
    query = request.GET.get("q")
    if query:
        students = (
            Student.objects.filter(name__icontains=query)
            | Student.objects.filter(email__icontains=query)
            | Student.objects.filter(course__icontains=query)
        )
    else:
        students = Student.objects.all()

    total_students = students.count()
    present_students = students.filter(is_present=True).count()
    absent_students = students.filter(is_present=False).count()

    return render(request, "students/home.html", {
        "students": students,
        "total_students": total_students,
        "present_students": present_students,
        "absent_students": absent_students,
    })

# ---------------- CRUD ----------------
@login_required
def add_student(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        passed_out = request.POST['passed_out']
        course = request.POST['course']
        is_present = request.POST.get('is_present') == "True"

        Student.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            passed_out=passed_out,
            course=course,
            is_present=is_present
        )
        messages.success(request, "✅ Student added successfully!")
        return redirect("home")

    return render(request, "students/add_student.html")

@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Student updated successfully!")
            return redirect("home")
    else:
        form = StudentForm(instance=student)
    return render(request, "students/edit_student.html", {"form": form})

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "🗑️ Student deleted successfully!")
    return redirect("home")

@login_required
def toggle_attendance(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.is_present = not student.is_present
        student.save()
        messages.success(request, f"Attendance updated for {student.name}")
    return redirect("home")