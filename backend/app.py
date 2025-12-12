"""
FastAPI Backend Server for Future-Self Recommendation System
Provides REST API endpoint for content recommendations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
import sys
from pathlib import Path

# Add backend directory to path to import recommender
sys.path.append(str(Path(__file__).parent))

from recommender import FutureSelfEngine

# Initialize FastAPI app
app = FastAPI(
    title="Future-Self Recommendation API",
    description="Goal-driven content recommendation system",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation engine
recommendation_engine = FutureSelfEngine()


# Request/Response Models
class RecommendationRequest(BaseModel):
    """Request model for recommendation endpoint"""
    goal: str = Field(
        ..., 
        description="User's future-self goal statement",
        min_length=3,
        example="I want to become a CTO"
    )
    top_k: int = Field(
        default=5,
        description="Number of recommendations to return",
        ge=1,
        le=20
    )


class ContentRecommendation(BaseModel):
    """Model for individual content recommendation"""
    title: str
    type: str
    description: str
    url: str
    match_score: float
    content_vector: List[float]


class RecommendationResponse(BaseModel):
    """Response model for recommendation endpoint"""
    user_goal: str
    goal_vector: List[float]
    skill_dimensions: List[str]
    recommendations: List[Dict]


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Future-Self Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "POST /recommend_content": "Get content recommendations based on your future-self goal",
            "GET /health": "Health check endpoint",
            "GET /stats": "Get system statistics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "engine": "operational",
        "content_items": len(recommendation_engine.content_metadata)
    }


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "total_content_items": len(recommendation_engine.content_metadata),
        "skill_dimensions": recommendation_engine.skill_dimensions,
        "content_types": recommendation_engine.content_metadata['Type'].value_counts().to_dict()
    }


@app.post("/recommend_content", response_model=RecommendationResponse)
async def recommend_content(request: RecommendationRequest):
    """
    Generate content recommendations based on user's future-self goal.
    
    Args:
        request: RecommendationRequest containing user's goal
    
    Returns:
        RecommendationResponse with goal vector and top recommendations
    
    Raises:
        HTTPException: If recommendation generation fails
    """
    try:
        # Validate input
        if not request.goal or request.goal.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Goal cannot be empty"
            )
        
        # Generate recommendations
        result = recommendation_engine.recommend(
            user_goal=request.goal.strip(),
            top_k=request.top_k
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@app.get("/content/all")
async def get_all_content():
    """Get all available content items"""
    try:
        content_df = recommendation_engine.data_loader.content_data
        return {
            "total_items": len(content_df),
            "content": content_df.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve content: {str(e)}"
        )


@app.get("/skills")
async def get_skill_dimensions():
    """Get all skill dimensions used in the system"""
    return {
        "skill_dimensions": recommendation_engine.skill_dimensions,
        "total_dimensions": len(recommendation_engine.skill_dimensions)
    }


# Run the application
if __name__ == "__main__":
    import uvicorn
    
    print("Starting Future-Self Recommendation API...")
    print("API Documentation available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
