# HRMS Lite – Backend

## Overview
This is the **backend service** for HRMS Lite — a lightweight Human Resource Management System.

It provides RESTful APIs to:
- Manage employees
- Track daily attendance

Built using **FastAPI** and **MongoDB (PyMongo)** with a focus on:
- Clean architecture
- Simple synchronous logic
- Stable APIs
- Deployment readiness

No authentication is implemented (single admin assumption).

---

## Live API
Backend URL:  
https://your-backend-url.onrender.com  



> Replace with your deployed link.

---

## Tech Stack
- **Backend Framework:** FastAPI
- **Database:** MongoDB Atlas
- **Driver:** PyMongo
- **Validation:** Pydantic
- **Server:** Uvicorn
- **Deployment:** Render / Railway

---

## Project Structure
backend/
├── app/
│ ├── main.py # FastAPI app entry
│ ├── db.py # MongoDB connection logic
│ ├── models.py # Database helpers
│ ├── schemas.py # Pydantic request/response models
│ └── routes/
│ ├── employees.py
│ └── attendance.py
├── requirements.txt
├── .env
└── README.md


---

## Features

### Employee Management
- Add employee (unique employeeId)
- View all employees
- Delete employee

### Attendance Management
- Mark attendance (date + status)
- View attendance per employee

---

## API Endpoints

### Employees
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees` | Get all employees |
| POST | `/employees` | Add new employee |
| DELETE | `/employees/{employeeId}` | Delete employee |

### Attendance
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/attendance` | Mark attendance |
| GET | `/attendance/{employeeId}` | View attendance records |

---

## Local Setup

### 1️⃣ Go to backend folder
```bash
cd backend

Create virtual environment
python -m venv venv
venv\Scripts\activate    

Install dependencies
pip install -r requirements.txt

Create a .env file:
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/hrms

Run server
uvicorn app.main:app --reload