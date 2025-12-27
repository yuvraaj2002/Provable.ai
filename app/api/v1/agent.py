from fastapi import Depends, HTTPException,APIRouter,status
from fastapi.responses import JSONResponse

router = APIRouter(prefix='/api/v1/agent',tags=['agent'])


@router.post("/evaluate-faithfulness")
async def evaluate_faithfulness():
    try:
        pass
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )