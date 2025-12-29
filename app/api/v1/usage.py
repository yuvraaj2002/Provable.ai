import traceback
from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from fastapi.responses import JSONResponse
from app.security.dependencies import get_current_auth_user
from app.core.database import get_db


router = APIRouter(prefix="/api/v1/usage",tags=["usage"])

@router.get("/faithfullness-usage-analytics")
async def faithfullness_usage_analytics(current_auth_user=Depends(get_current_auth_user),db_session=Depends(get_db)):
    try:
        
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in usage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )