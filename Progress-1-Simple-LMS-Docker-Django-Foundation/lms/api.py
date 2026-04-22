from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError

# Semua import diarahkan ke folder 'courses'
from courses.models import Course, Enrollment, Progress, Lesson, User
from courses.schemas import (
    UserRegisterIn, 
    UserOut, 
    CourseIn, 
    CourseOut, 
    EnrollmentOut, 
    EnrollmentIn
)
from courses.utils import role_required

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

# POST User
@api.post("/auth/login", tags=["auth"])
def login(request):
    # Ini akan memanggil fungsi login JWT kamu
    pass

@api.post("/auth/refresh", tags=["auth"])
def refresh(request):
    # Ini untuk refresh token
    pass



@api.post("/auth/register", response=UserOut, auth=None)
def register(request, data: UserRegisterIn):
    user = User.objects.create_user(**data.dict())
    return user

@api.get("/auth/me", auth=JWTAuth(), response=UserOut)
def me(request):
    return request.user

@api.put("/auth/me", auth=JWTAuth(), response=UserOut)
def update_me(request, data: UserRegisterIn): # Pakai schema yang ada atau buat baru
    user = request.user
    for attr, value in data.dict(exclude={'password'}).items():
        setattr(user, attr, value)
    if data.password:
        user.set_password(data.password)
    user.save()
    return user


# --- COURSES ---

@api.get("/courses", response=list[CourseOut])
def list_courses(request):
    return Course.objects.for_listing()


@api.post("/courses", auth=JWTAuth(), response=CourseOut)
@role_required(['instructor', 'admin'])
def create_course(request, data: CourseIn):
    # Buat objek course
    course = Course.objects.create(instructor=request.user, **data.dict())
    return course

@api.patch("/courses/{course_id}", auth=JWTAuth(), response=CourseOut)
def update_course(request, course_id: int, data: CourseIn):
    course = get_object_or_404(Course, id=course_id)
    
    if course.instructor != request.user and request.user.role != 'admin':
        # Menggunakan format return (status_code, dict) yang benar untuk Ninja
        raise HttpError(403, "Bukan pemilik course")
    
    for attr, value in data.dict().items():
        setattr(course, attr, value)
    course.save()
    return course

@api.get("/courses/{course_id}", response=CourseOut) 
def get_course_detail(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    return course

# --- ENROLLMENTS & PROGRESS ---
# --- ENROLLMENTS ---

@api.post("/enrollments", auth=JWTAuth(), response=EnrollmentOut)
@role_required(['student'])
def enroll_course(request, data: EnrollmentIn):
    # Cek apakah sudah terdaftar
    if Enrollment.objects.filter(course_id=data.course_id, student=request.user).exists():
        raise HttpError(400, "Kamu sudah terdaftar di kursus ini")
    
    enrollment = Enrollment.objects.create(
        course_id=data.course_id,
        student=request.user
    )
    return enrollment

@api.get("/enrollments/my-courses", auth=JWTAuth(), response=list[EnrollmentOut])
def my_courses(request):
    return Enrollment.objects.filter(student=request.user)

@api.post("/enrollments/{enrollment_id}/progress", auth=JWTAuth())
def mark_lesson_complete(request, enrollment_id: int, lesson_id: int):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=enrollment.course)
    
    progress, created = Progress.objects.update_or_create(
        enrollment=enrollment,
        lesson=lesson,
        defaults={'completed': True}
    )
    return {"message": f"Lesson {lesson.title} completed"}

@api.delete("/courses/{course_id}", auth=JWTAuth())
@role_required(['admin'])
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return {"success": True}