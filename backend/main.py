from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.routers import schools, classes, subjects, teachers, timetables, auth
from app.database import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Timetable Generator API",
    description="A comprehensive API for generating and managing school timetables",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(schools.router, prefix="/api/schools", tags=["Schools"])
app.include_router(classes.router, prefix="/api/classes", tags=["Classes"])
app.include_router(subjects.router, prefix="/api/subjects", tags=["Subjects"])
app.include_router(teachers.router, prefix="/api/teachers", tags=["Teachers"])
app.include_router(timetables.router, prefix="/api/timetables", tags=["Timetables"])

@app.get("/")
async def root():
    return {"message": "School Timetable Generator API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
