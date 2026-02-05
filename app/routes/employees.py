from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from app.db import db
from app.schemas import EmployeeCreate, Employee

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.post("/add_employee", status_code=201)
def create_employee(employee: EmployeeCreate):
    # Check for duplicate emp_id or email
    if db.employees.find_one({"emp_id": employee.employeeId}):
        raise HTTPException(status_code=200, detail="Employee ID already exists")
    
    if db.employees.find_one({"email": employee.email}):
        raise HTTPException(status_code=200, detail="Email already exists")
    
    data = {
        "emp_id": employee.employeeId,
        "name": employee.fullName,
        "email": employee.email,
        "department": employee.department
    }
    result = db.employees.insert_one(data)
    return {
        "message": "Employee added successfully",
        "employee": {
            "id": str(result.inserted_id),
            **employee.dict()
        }
    }


@router.get("/list/", response_model=list[Employee])
def get_employees():
    print("Fetching employees from database...")
    print(f"Database name: {db.name}")
    print(f"Collections in database: {db.list_collection_names()}")
    
    # Check all collections for data
    for collection_name in db.list_collection_names():
        count = db[collection_name].count_documents({})
        print(f"Collection '{collection_name}' has {count} documents")
        if count > 0:
            sample = db[collection_name].find_one({})
            print(f"Sample document from '{collection_name}': {sample}")
    
    employees = list(db.employees.find({}))
    print(f"Found {len(employees)} employees")
    
    if not employees:
        return []
    
    for emp in employees:
        emp["id"] = str(emp["_id"])
        emp["employeeId"] = emp.pop("emp_id")
        emp["fullName"] = emp.pop("name")
        del emp["_id"]
    
    return employees


@router.get("/", response_model=list[Employee])
def get_employees_alt():
    employees = list(db.employees.find({}))
    for emp in employees:
        emp["id"] = str(emp["_id"])
        emp["employeeId"] = emp.pop("emp_id")
        emp["fullName"] = emp.pop("name")
        del emp["_id"]
    return employees


@router.delete("/delete_employee/{employeeId}", status_code=200)
def delete_employee(employeeId: str):
    from bson import ObjectId
    try:
        result = db.employees.delete_one({"_id": ObjectId(employeeId)})
    except:
        result = db.employees.delete_one({"emp_id": employeeId})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully", "status": "success"}


@router.put("/edit_employee/{employeeId}", status_code=200)
def update_employee(employeeId: str, employee: EmployeeCreate):
    from bson import ObjectId
    
    # Check for duplicate emp_id (excluding current employee)
    existing_emp_id = db.employees.find_one({"emp_id": employee.employeeId})
    if existing_emp_id and str(existing_emp_id["_id"]) != employeeId:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    # Check for duplicate email (excluding current employee)
    existing_email = db.employees.find_one({"email": employee.email})
    if existing_email and str(existing_email["_id"]) != employeeId:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    data = {
        "emp_id": employee.employeeId,
        "name": employee.fullName,
        "email": employee.email,
        "department": employee.department
    }
    
    try:
        result = db.employees.update_one({"_id": ObjectId(employeeId)}, {"$set": data})
    except:
        result = db.employees.update_one({"emp_id": employeeId}, {"$set": data})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return {
        "message": "Employee updated successfully",
        "employee": {
            "id": employeeId,
            **employee.dict()
        }
    }
