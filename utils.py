# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import jwt
#
# SECRET_KEY = 'SECRET_KEY_123'
# ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({'exp': expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
#
# pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
#
#
# def hash_password(password: str):
#     return pwd_context.hash(password)
#
#
