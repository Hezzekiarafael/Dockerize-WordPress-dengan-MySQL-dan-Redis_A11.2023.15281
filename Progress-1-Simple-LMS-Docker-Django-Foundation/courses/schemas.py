from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- SCHEMAS USER ---
class UserRegisterIn(BaseModel):
    username: str
    password: str
    email: str
    role: str = "student"

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True # <--- TAMBAHKAN INI DI USEROUT JUGA
        orm_mode = True        # Tambahkan ini untuk jaga-jaga versi pydantic

# --- SCHEMAS COURSE ---
class CourseIn(BaseModel):
    title: str
    description: str
    category_id: Optional[int] = None

class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    instructor: UserOut # UserOut sekarang sudah bisa baca data ORM

    class Config:
        from_attributes = True
        orm_mode = True

# --- SCHEMAS ENROLLMENT ---
class EnrollmentIn(BaseModel):
    course_id: int

class EnrollmentOut(BaseModel):
    id: int
    course_id: int
    student_id: int
    enrolled_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True