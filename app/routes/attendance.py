from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas import AttendanceCreate, Attendance
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.post("/", response_model=Attendance)
def mark_attendance(attendance: AttendanceCreate):
    if not db.employees.find_one({"employeeId": attendance.employeeId}):
        raise HTTPException(status_code=404, detail="Employee not found")

    date_dt = datetime.combine(attendance.date, datetime.min.time())

    existing = db.attendance.find_one({
        "employeeId": attendance.employeeId,
        "date": date_dt
    })
    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")

    data = attendance.dict()
    data["date"] = date_dt

    result = db.attendance.insert_one(data)

    return {
        "id": str(result.inserted_id),
        **data
    }


@router.post("/update_attendance")
def update_attendance(attendance: AttendanceCreate):
    # Check if employeeId is MongoDB ObjectId or emp_id
    employee = None
    try:
        employee = db.employees.find_one({"_id": ObjectId(attendance.employeeId)})
    except:
        employee = db.employees.find_one({"emp_id": attendance.employeeId})
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    emp_id = employee.get("emp_id")
    date_dt = datetime.combine(attendance.date, datetime.min.time())

    result = db.attendance.update_one(
        {"employeeId": emp_id, "date": date_dt},
        {"$set": {"status": attendance.status}},
        upsert=True
    )

    return {"message": "Attendance updated successfully", "modified": result.modified_count, "upserted": result.upserted_id is not None}


@router.get("/{employeeId}", response_model=list[Attendance])
def get_attendance(employeeId: str):
    records = list(db.attendance.find({"employeeId": employeeId}))
    for r in records:
        r["id"] = str(r["_id"])
        del r["_id"]
    return records
