from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    hash_val = pwd_context.hash("test")
    print("Hash successful:", hash_val)
except Exception as e:
    print("Exception type:", type(e))
    print("Exception:", e)
