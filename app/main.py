import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.employees import router as employees_router
from app.routes.attendance import router as attendance_router

app = FastAPI(title="HRMS Lite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees_router)
app.include_router(attendance_router)

@app.get("/")
def home():
    return {"message": "HRMS Lite Backend Running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
