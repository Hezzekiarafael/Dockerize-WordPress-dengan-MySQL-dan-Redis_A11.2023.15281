import os
import django
from django.db import connection, reset_queries

# Pastikan 'lms.settings' sesuai dengan nama folder tempat file settings.py kamu berada
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings') 
django.setup()

from courses.models import Course

def run_query_demo():
    print("\n" + "="*60)
    print("DEMO 1: NAIVE QUERY (Tanpa Optimasi / N+1 Problem)")
    print("="*60)
    reset_queries() # Reset penghitung query
    
    # Query biasa (Buruk untuk performa)
    naive_courses = Course.objects.all()
    for course in naive_courses:
        # Mengakses relasi instructor dan category memicu query baru
        print(f"Course: {course.title} | Dosen: {course.instructor.username}")
        # Mengakses lesson memicu query baru lagi
        for lesson in course.lessons.all():
            print(f"   - Lesson: {lesson.title}")
            
    naive_count = len(connection.queries)
    print(f"\n TOTAL QUERY KE DATABASE: {naive_count}\n")


    print("="*60)
    print("DEMO 2: OPTIMIZED QUERY (Dengan select_related & prefetch_related)")
    print("="*60)
    reset_queries() # Reset penghitung query
    
    # Query optimasi memanggil custom manager (for_listing) yang kamu buat di models.py
    optimized_courses = Course.objects.for_listing()
    for course in optimized_courses:
        print(f" Course: {course.title} | Dosen: {course.instructor.username}")
        for lesson in course.lessons.all():
            print(f"   - Lesson: {lesson.title}")
            
    optimized_count = len(connection.queries)
    print(f"\n TOTAL QUERY KE DATABASE: {optimized_count}\n")
    
    print("="*60)
    print(f"KESIMPULAN: Optimasi berhasil menghemat {naive_count - optimized_count} queries!")
    print("="*60 + "\n")

if __name__ == '__main__':
    run_query_demo()