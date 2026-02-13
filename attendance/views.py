from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Student, Attendance
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.http import HttpResponse
import qrcode 


# ================= Home (عام، بدون تسجيل دخول) =================
def home(request):
    return render(request, "attendance/home.html")

# ================= إضافة طالب =================
@login_required
def add_student(request):
    message = ""
    message_class = ""
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        student_code = request.POST.get("student_code")
        birth_year = request.POST.get("birth_year")
        class_name = request.POST.get("class_name")
        if Student.objects.filter(student_code=student_code).exists():
            message = "❌ الطالب موجود مسبقًا"
            message_class = "error"
        else:
            Student.objects.create(
                full_name=full_name,
                student_code=student_code,
                birth_year=birth_year,
                class_name=class_name
            )
            message = "✅ تم إضافة الطالب بنجاح"
            message_class = "success"
    return render(request, "attendance/add_student.html", {"message": message, "message_class": message_class})

# ================= تسجيل حضور / غياب =================
def register_attendance(request):
    message = ""
    if request.method == "POST":
        student_code = request.POST.get("student_code")
        status = request.POST.get("status")
        try:
            student = Student.objects.get(student_code=student_code)
            today_attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=timezone.localdate()
            )
            if status == "present":
                today_attendance.time_in = timezone.now()
                message = f"{student.full_name} ✅ تم تسجيل حضوره"
            elif status == "absent":
                today_attendance.time_out = timezone.now()
                message = f"{student.full_name} ❌ تم تسجيل غيابه"
            today_attendance.save()
        except Student.DoesNotExist:
            message = "❌ الطالب غير موجود"
    return render(request, "attendance/register.html", {"message": message})

# ================= عرض الغيابات (محمي) =================
@login_required
def view_attendance(request):
    attendances = Attendance.objects.select_related('student').order_by('-date')
    return render(request, "attendance/view_attendance.html", {"attendances": attendances, "today": timezone.localdate()})

# ================= تسجيل دخول المدير =================
def admin_login(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("home")
        else:
            message = "❌ اسم المستخدم أو كلمة المرور غير صحيحة"
    return render(request, "attendance/admin_login.html", {"message": message})

# ================= تسجيل خروج المدير =================
@login_required
def admin_logout(request):
    logout(request)
    return redirect("home")

@login_required
def view_students(request):
    students = Student.objects.all()
    return render(request, "attendance/view_students.html", {"students": students})

@login_required
def generate_qr(request):
    """
    صفحة لإنشاء QR Code للطالب باستخدام الرقم المدرسي
    """
    qr_image_url = None

    if request.method == "POST":
        student_code = request.POST.get("student_code")
        try:
            student = Student.objects.get(student_code=student_code)
        except Student.DoesNotExist:
            student = None

        if student:
            # إنشاء QR Code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(student.student_code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # تحويل الصورة لبايت
            buffer = BytesIO()
            img.save(buffer, "PNG")
            buffer.seek(0)

            # إرسال الصورة كملف للتحميل
            response = HttpResponse(buffer, content_type="image/png")
            response['Content-Disposition'] = f'attachment; filename={student.student_code}.png'
            return response

    return render(request, "attendance/generate_qr.html")
