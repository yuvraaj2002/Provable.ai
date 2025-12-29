import traceback
from app.models.agent_faithfullness import AgentFaithfullness
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class AnalyticsService():
    def __init__(self):
        pass

    async def get_faithfullness_analytics(self,user_id:str,db_session:AsyncSession):
        try:
            # Getting all data associated with current user id
            result = await db_session.execute(select(AgentFaithfullness).where(AgentFaithfullness.user_id == user_id))
            result = result.all()
        except Exception as e:
            traceback.print_exc()
            return None