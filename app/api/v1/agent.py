from fastapi import Depends, HTTPException,APIRouter,status
from fastapi.responses import JSONResponse
from app.schema.agent_schema import EvaluateFaithfulnessRequest
from app.security.dependencies import get_current_user_from_api_key

router = APIRouter(prefix='/api/v1/agent',tags=['agent'])


@router.post("/evaluate-faithfulness")
async def evaluate_faithfulness(request: EvaluateFaithfulnessRequest, current_auth_user=Depends(get_current_user_from_api_key)):
    try:
        # TODO : Check current subscription, deduct credits, perform action
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