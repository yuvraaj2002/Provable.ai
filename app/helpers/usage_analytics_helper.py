from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.agent_faithfullness import AgentFaithfullness
from typing import List, Dict, Any

class UsageAnalyticsHelper():

    def __init__(self):
        pass

    def _serialize_faithfulness_record(self, record: AgentFaithfullness) -> Dict[str, Any]:
        """Convert SQLAlchemy model to dictionary for JSON serialization."""
        return {
            "id": record.id,
            "user_id": record.user_id,
            "query": record.query,
            "context_retrieved": record.context_retrieved,
            "response": record.response,
            "verification_claims": record.verification_claims,
            "total_claims": record.total_claims,
            "supported_claims": record.supported_claims,
            "non_supported_claims": record.non_supported_claims,
            "created_at": record.created_at.isoformat() if record.created_at else None
        }

    async def _get_faithfullness_usage(self,user_id:str,db_session:AsyncSession) -> List[Dict[str, Any]]:
        try:
            # Getting all data associated with current user id
            result = await db_session.execute(select(AgentFaithfullness).where(AgentFaithfullness.user_id == user_id))
            records = result.scalars().all()
            # Serialize SQLAlchemy objects to dictionaries
            return [self._serialize_faithfulness_record(record) for record in records]
        except Exception as e:
            print(f"Error in _get_faithfullness_usage: {e}")
            import traceback
            traceback.print_exc()
            return None