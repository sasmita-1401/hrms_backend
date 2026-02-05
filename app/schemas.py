from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# Employee Schemas
class EmployeeBase(BaseModel):
    employeeId: str = Field(..., example="EMP001")
    fullName: str = Field(..., example="John Doe")
    email: EmailStr
    department: str = Field(..., example="HR")

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: Optional[str]  # MongoDB _id

# Attendance Schemas
class AttendanceBase(BaseModel):
    employeeId: str = Field(..., example="EMP001")
    date: date
    status: str = Field(..., example="Present")

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: Optional[str]
