#!/usr/bin/env python3
"""
Startup script for the School Timetable Generator Backend
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting School Timetable Generator Backend...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🌐 Server: http://localhost:8000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
