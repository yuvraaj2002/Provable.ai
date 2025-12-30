from fastapi import Depends, HTTPException,APIRouter,status
from fastapi.responses import JSONResponse
from app.schema.evaluate_generator_schema import EvaluateGeneratorRequest
from app.schema.pii_registeration_schema import PIIRegisteration
from app.security.dependencies import get_current_user_from_api_key,get_current_auth_user
from app.services.llm_service import LLMService
from app.core.database import get_db
from app.helpers import PIIRegisterationHelper

router = APIRouter(prefix='/api/v1/agent',tags=['agent'])
llm_service = LLMService()
pii_helper = PIIRegisterationHelper()


@router.post("/evaluate-generator")
async def evaluate_faithfulness(request: EvaluateGeneratorRequest, current_auth_user=Depends(get_current_user_from_api_key)):
    try:
        # TODO : Check current subscription, deduct credits, perform action
        
        # Analyze faithfulness and extract claims
        result = await llm_service.evaluate_generator(request)
        
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


@router.post("/pii-registeration")
async def pii_registeration(request:PIIRegisteration,current_auth_user=Depends(get_current_auth_user),db_session=Depends(get_db)):
    try:
        result = await pii_helper.register_pii_details(current_auth_user.id, request, db_session)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register PII details for analysis."
            )
        
        return JSONResponse(content={'message':'PII Registered successfully'},status=status.HTTP_200_OK)
 
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error in agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )