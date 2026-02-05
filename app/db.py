from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "demohrms")

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Create unique index for employees collection
try:
    db.employees.create_index("employeeId", unique=True)
except Exception as e:
    print("Employee index creation skipped:", e)

# Create compound index for attendance collection (employeeId + date)
try:
    db.attendance.create_index([("employeeId", 1), ("date", 1)], unique=True)
except Exception as e:
    print("Attendance index creation skipped:", e)
