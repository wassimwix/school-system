from django.urls import path
from .views import (
    register_attendance, add_student, admin_login,
    admin_logout, view_attendance, home, view_students ,generate_qr )
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", home, name="home"),
    path("register/", register_attendance, name="register"),
    path("add/", add_student, name="add_student"),
    path("view/", view_attendance, name="view_attendance"),
    path("students/", view_students, name="view_students"), 
    path("login/", admin_login, name="admin_login"),
    path("logout/", admin_logout, name="admin_logout"),
    path("generate_qr/", generate_qr, name="generate_qr"),
]
