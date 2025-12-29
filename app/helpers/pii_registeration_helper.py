from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.pii_registeration_schema import PIIRegisteration
from app.models.pii_detection import PII_Registeration

class PIIRegisterationHelper():

    def __init__(self):
        pass

    async def register_pii_details(self,user_id:str,registeration_data:PIIRegisteration,db_session:AsyncSession):
        try:
            # Creating instance of the PII_Registeration table
            pii_registeration = PII_Registeration(
                user_id = user_id,
                endpoint_url = registeration_data.endpoint_url,
                bearer_token = registeration_data.bearer_token,
                description = registeration_data.description,
                email_alert = registeration_data.email_alert
            )
            db_session.add(pii_registeration)
            await db_session.commit()
            await db_session.refresh(pii_registeration)
            return True
        except Exception as e:
            await db_session.rollback()
            return False