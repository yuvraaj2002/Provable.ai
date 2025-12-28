from fastapi import Depends, HTTPException,APIRouter,status
from fastapi.responses import JSONResponse
from app.schema.agent_schema import EvaluateFaithfulnessRequest
from app.security.dependencies import get_current_user_from_api_key
from app.services.llm_service import LLMService

router = APIRouter(prefix='/api/v1/agent',tags=['agent'])
llm_service = LLMService()


@router.post("/evaluate-faithfulness")
async def evaluate_faithfulness(request: EvaluateFaithfulnessRequest, current_auth_user=Depends(get_current_user_from_api_key)):
    try:
        # TODO : Check current subscription, deduct credits, perform action
        
        # Analyze faithfulness and extract claims
        result = await llm_service.analyze_faithfulness(request)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to extract claims from the response."
            )
        
        # Result is already in the correct format from the service
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in agent: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )