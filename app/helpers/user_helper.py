from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from sqlalchemy.sql import func
from sqlalchemy import select, update
from app.security.jwt_management import create_access_token
from app.security.password_management import verify_password

class UserHelper:
    
    async def get_or_create(self, user_data: dict, db_session: AsyncSession):
        try:
            google_sub = user_data['sub']  
            result = await db_session.execute(select(User).where(User.id == google_sub))
            user = result.scalar_one_or_none()
            
            if user:
                # User exists so its login attempt, update last_login
                user.last_login = func.now()
                await db_session.commit()

                # Creating access token
                data = {"id":user.id,"email":user.email}
                access_token =await create_access_token(data)
                return access_token
            else:
                # Signup attempt, create new user
                new_user = User(
                    id=google_sub,
                    email=user_data['email'],
                    name=user_data['name'],
                    profile_picture=None
                )
                db_session.add(new_user)
                await db_session.commit()
                await db_session.refresh(new_user)

                 # Creating access token
                data = {"id":new_user.id,"email":new_user.email}
                access_token =await create_access_token(data)
                return access_token
        
        except Exception as e:
            print(f"Error in get_or_create: {e}")
            await db_session.rollback()
            return None

    async def create_user(self, user_data: dict, db_session: AsyncSession):
        try:
            new_user = User(
                id=user_data['google_sub'],
                email=user_data['email'],
                name=user_data.get('name'),
                profile_picture=user_data.get('profile_picture')
            )
            db_session.add(new_user)
            await db_session.commit()
            await db_session.refresh(new_user)
            return new_user
        except Exception as e:
            print(f"Error creating user: {e}")
            await db_session.rollback()
            return None

    async def get_user(self, user_id: str, db_session: AsyncSession):
        try:
            result = await db_session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    async def verify_password_generate_token(hashed_password:str):
        try:
            if not verify_password(hashed_password):
                return None
            else:
                
                create_access_token()
        except Exception as e:
            return None
    
    async def update_user(self, user_id: str, update_data: dict, db_session: AsyncSession):
        try:
            await db_session.execute(
                update(User).where(User.id == user_id).values(**update_data)
            )
            await db_session.commit()
            return await self.get_user(user_id, db_session)
        except Exception as e:
            print(f"Error updating user: {e}")
            await db_session.rollback()
            return None
