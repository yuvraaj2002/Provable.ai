import uuid
from app.models.api_keys import ApiKeys
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.security.password_management import PasswordManagement


class ApiKeyHelper():
    def __init__(self):
        self.password_management = PasswordManagement()

    async def create_key(self,key_name:str,user_id:str,db_session:AsyncSession):
        try:
            # Generating new secret key with the format sk_live_ + random uuid
            secret_key = "sk_live_" + str(uuid.uuid4())

            # Getting the last 4 digits and creating the hash
            last_4_digit = secret_key[-4:]
            hashed_key = self.password_management.hash_password(password=secret_key)

            new_api_key = ApiKeys(user_id=user_id,key_name=key_name,hash_key=hashed_key,last_4_digit=last_4_digit)
            db_session.add(new_api_key)
            await db_session.commit()
            await db_session.refresh(new_api_key)
            return secret_key

        except Exception as e:
            await db_session.rollback()
            return None

    async def get_keys(self,user_id:str,db_session:AsyncSession):
        try:
            result = await db_session.execute(select(ApiKeys).where(ApiKeys.user_id == user_id))
            api_keys = result.scalars().all()
            
            keys_info = []
            for api_key in api_keys:
                keys_info.append({
                    "id": api_key.id,
                    "key_name": api_key.key_name,
                    "last_4_digit": api_key.last_4_digit,
                    "created_at": api_key.created_at.isoformat() if api_key.created_at else None
                })
            return keys_info
        except Exception as e:
            return None


    async def delete_key(self,key_id:str,user_id:str,db_session:AsyncSession):
        try:
            # Find the API key and verify it belongs to the user
            result = await db_session.execute(
                select(ApiKeys).where(ApiKeys.id == key_id, ApiKeys.user_id == user_id)
            )
            api_key = result.scalar_one_or_none()
            
            if api_key is None:
                return False
            
            db_session.delete(api_key)
            await db_session.commit()
            return True

        except Exception as e:
            await db_session.rollback()
            return False