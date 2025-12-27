import bcrypt

class PasswordManagement():

    def __init__(self):
        pass

    def hash_password(self, password: str):
        try:
            # Generate salt and hash password using bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed_password.decode('utf-8')
        except Exception as e:
            print(f"Error hashing password: {e}")
            raise ValueError(f"Failed to hash password: {e}") from e

    def verify_password(self, login_password_attempt: str, hashed_password: str):
        try:
            if not hashed_password:
                return False
            # Verify password using bcrypt
            return bcrypt.checkpw(
                login_password_attempt.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False