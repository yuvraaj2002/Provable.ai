import traceback
from fastapi import FastAPI,APIRouter,HTTPException,status,Depends
from fastapi.responses import JSONResponse
from app.security.dependencies import get_current_auth_user
from app.core.database import get_db
from app.helpers import UsageAnalyticsHelper


router = APIRouter(prefix="/api/v1/usage",tags=["usage"])
usage_analytics_helper = UsageAnalyticsHelper()

@router.get("/faithfullness-usage-analytics")
async def faithfullness_usage_analytics(current_auth_user=Depends(get_current_auth_user),db_session=Depends(get_db)):
    try:
        result = await usage_analytics_helper._get_faithfullness_usage(current_auth_user.id,db_session)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve faithfulness usage analytics."
            )
        return JSONResponse(content={"data": result},status_code=status.HTTP_200_OK)
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in usage: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )