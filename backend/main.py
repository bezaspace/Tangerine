from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import os
from dotenv import load_dotenv

from models import Practitioner, PractitionerResponse
from database import PractitionerDatabase

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Tangerine Practitioners API",
    description="API for Ayurvedic practitioners in the Tangerine app",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    PractitionerDatabase.initialize_database()

# Configure CORS for React Native app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Tangerine Practitioners API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "practitioners-api"}

@app.get("/api/practitioners", response_model=PractitionerResponse)
async def get_practitioners(
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    location: Optional[str] = Query(None, description="Filter by location"),
    limit: Optional[int] = Query(10, description="Limit number of results")
):
    """Get all practitioners with optional filtering"""
    try:
        if specialty or location:
            practitioners = PractitionerDatabase.search_practitioners(specialty=specialty, location=location)
        else:
            practitioners = PractitionerDatabase.get_all_practitioners()
        
        # Apply limit
        limited_practitioners = practitioners[:limit] if limit else practitioners
        
        return PractitionerResponse(
            practitioners=limited_practitioners,
            total=len(practitioners)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching practitioners: {str(e)}")

@app.get("/api/practitioners/{practitioner_id}", response_model=Practitioner)
async def get_practitioner(practitioner_id: int):
    """Get a specific practitioner by ID"""
    try:
        practitioner = PractitionerDatabase.get_practitioner_by_id(practitioner_id)
        if not practitioner:
            raise HTTPException(status_code=404, detail="Practitioner not found")
        return practitioner
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching practitioner: {str(e)}")

@app.get("/api/practitioners/search", response_model=PractitionerResponse)
async def search_practitioners(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, description="Limit number of results")
):
    """Search practitioners by name or specialty"""
    try:
        all_practitioners = PractitionerDatabase.get_all_practitioners()
        
        # Simple search implementation
        search_results = [
            p for p in all_practitioners 
            if q.lower() in p.name.lower() or q.lower() in p.specialty.lower()
        ]
        
        # Apply limit
        limited_results = search_results[:limit] if limit else search_results
        
        return PractitionerResponse(
            practitioners=limited_results,
            total=len(search_results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching practitioners: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)