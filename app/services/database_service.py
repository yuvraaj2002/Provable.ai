# from app.core.database import get_db
# from app.models.users import User

# class DatabaseService:
    
#     def create_user(self, user_data):
#         try:
#             with get_db() as db_session:
#                 new_user = User(**user_data)
#                 db_session.add(new_user)
#                 db_session.commit()
#                 db_session.refresh(new_user)
#                 return new_user
#         except Exception as e:
#             print(f"Error creating user: {e}")
#             return None    

#     def get_user(self, user_id):
#         try:
#             with get_db() as db_session:
#                 db_session.
#         except Exception as e:
#             print(f"Error creating user: {e}")
#             return None 
        
#     def update_user(self, user_id, update_data):
#         try:
#             with get_db() as db_session:
#                 pass
#         except Exception as e:
#             print(f"Error creating user: {e}")
#             return None 