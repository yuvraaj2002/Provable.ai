import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import PendingUser, User
from sqlalchemy.sql import func
from sqlalchemy import select, update
from app.security.jwt_management import create_access_token
from app.security.password_management import PasswordManagement
from app.services.email_service import send_verification_email

class UserHelper:
    def __init__(self):
        self.password_management = PasswordManagement()
    
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

    async def create_pending_user(self, username:str,email:str,hashed_password:str, db_session: AsyncSession):
        try:
            # Check if email already exists in User table
            existing_user = await db_session.execute(select(User).where(User.email == email))
            if existing_user.scalar_one_or_none() is not None:
                return None  # Email already registered
            
            # Check if email already exists in PendingUser table
            existing_pending = await db_session.execute(select(PendingUser).where(PendingUser.email == email))
            if existing_pending.scalar_one_or_none() is not None:
                return None  # Email already has pending verification
            
            # Creating UUID for the id in the PendingUser table
            pending_user_id = str(uuid.uuid4())
            # Creating verification token with pending user id and email
            data = {'id': pending_user_id, 'email': email}
            verification_token = await create_access_token(data)

            # Check if token creation failed
            if verification_token is None:
                return None

            new_pending_user = PendingUser(
                id=pending_user_id,  # Explicitly set the id
                email=email,
                name=username,
                hashed_password=hashed_password,
                verification_token=verification_token
            )
            db_session.add(new_pending_user)
            await db_session.commit()
            await db_session.refresh(new_pending_user)

            # Sending the verification mail
            email_sent = send_verification_email(email, username, verification_token)
            if not email_sent:
                print(f"Warning: Failed to send verification email to {email}")
                # Still return True as user was created successfully
                # Email failure can be handled separately if needed
            
            return True

        except Exception as e:
            print(f"Error creating pending user: {e}")
            await db_session.rollback()
            return None

    async def move_pending_user(self, pending_user_id: str, db_session: AsyncSession):
        try:
            # Finding the record of the user in pending user table
            result = await db_session.execute(select(PendingUser).where(PendingUser.id == pending_user_id))
            pending_user = result.scalar_one_or_none()
            
            # Check if pending user exists
            if pending_user is None:
                print(f"Pending user not found: {pending_user_id}")
                return False
            
            # Check if user already exists (might have been verified before)
            existing_user = await db_session.execute(select(User).where(User.email == pending_user.email))
            if existing_user.scalar_one_or_none() is not None:
                print(f"User already exists: {pending_user.email}")
                # Delete the pending user record since user already exists
                await db_session.delete(pending_user)
                await db_session.commit()
                return True 
            
            # Create new record in user table
            # Use the pending_user_id as the user id
            new_user = User(
                id=pending_user_id,  # Use the same ID from pending user
                email=pending_user.email,
                name=pending_user.name,
                hashed_password=pending_user.hashed_password,
                profile_picture=None
            )
            
            db_session.add(new_user)
            
            # Delete the pending user record after successful creation
            await db_session.delete(pending_user)
            
            await db_session.commit()
            await db_session.refresh(new_user)
            
            return True

        except Exception as e:
            print(f"Error moving pending user: {e}")
            await db_session.rollback()
            return False

    async def get_user(self, user_id: str, db_session: AsyncSession):
        try:
            result = await db_session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    async def verify_password_generate_token(self,email:str,login_attempt_password:str,db_session:AsyncSession):
        try:
            # Getting the user object (not just hashed_password) to access id and email
            result = await db_session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            # Check if user exists
            if user is None:
                return None
            
            # Verify the password
            if self.password_management.verify_password(login_attempt_password, user.hashed_password):
                # Update last_login timestamp
                user.last_login = func.now()
                await db_session.commit()
                
                # Creating the jwt token with user data
                data = {"id": user.id, "email": user.email}
                access_token = await create_access_token(data)
                return access_token
            else:
                # Password verification failed
                return None
        except Exception as e:
            print(f"Error in verify_password_generate_token: {e}")
            await db_session.rollback()
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
