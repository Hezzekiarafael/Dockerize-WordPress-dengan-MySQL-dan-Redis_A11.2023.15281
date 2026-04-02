from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Course, Lesson, Enrollment, Progress, User

# === 1. ADMIN USER CUSTOM ===
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')

# === 2. INLINE LESSON ===
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

# === 3. ADMIN COURSE ===
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category')
    search_fields = ('title', 'instructor__username', 'category__name') 
    list_filter = ('category', 'instructor')
    inlines = [LessonInline]

# === 4. ADMIN CATEGORY ===
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

# === 5. ADMIN ENROLLMENT ===
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('student__username', 'course__title')
    
# === 6. ADMIN PROGRESS ===
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'get_course', 'lesson', 'completed')
    list_filter = ('completed', 'enrollment__course')
    
    def get_student(self, obj):
        return obj.enrollment.student
    get_student.short_description = 'Student'
    
    def get_course(self, obj):
        return obj.enrollment.course
    get_course.short_description = 'Course'