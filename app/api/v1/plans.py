from fastapi import FastAPI, APIRouter, HTTPException, Request, Depends,status
from fastapi.responses import JSONResponse
from app.security.dependencies import get_current_admin_user

router = APIRouter(prefix="api/v1/plans",tags=["plans"])

@router.get("/get-plan-details")
async def get_plan(admin_user=Depends(get_current_admin_user)):
    try:
        pass
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in plans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.post('/add-new-plan')
async def create_plan(admin_user=Depends(get_current_admin_user)):
    try:
        pass
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in plans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.update("/update-plan")
async def update_plan(admin_user=Depends(get_current_admin_user)):
    try:
        pass
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in plans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete("/delete-plan")
async def delete_plan(admin_user=Depends(get_current_admin_user)):
    try:
        pass
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in plans: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
