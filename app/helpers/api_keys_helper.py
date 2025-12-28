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

    async def verify_api_key(self, api_key: str, db_session: AsyncSession):
        """
        Verify an API key against the database.
        Returns the user_id if valid, None otherwise.
        """
        try:
            # Extract last 4 digits from the provided API key for quick filtering
            if len(api_key) < 4:
                print("API key too short")
                return None
            
            # Extracting the last 4 digit and lookup in the database
            last_4_digit = api_key[-4:]
            result = await db_session.execute(select(ApiKeys).where(ApiKeys.last_4_digit == last_4_digit))
            api_keys = result.scalars().all()
            
            if not api_keys:
                print(f"No API keys found with last 4 digits: {last_4_digit}")
                return None
            
            # Verify the API key against each matching hash and returning the user id against matching one
            for api_key_record in api_keys:
                if self.password_management.verify_password(api_key, api_key_record.hash_key):
                    print(f"API key verified successfully for user: {api_key_record.user_id}")
                    return api_key_record.user_id
            
            print("API key verification failed - no matching hash found")
            return None
            
        except Exception as e:
            print(f"Error verifying API key: {e}")
            import traceback
            traceback.print_exc()
            return None