from fastapi import APIRouter, status, Depends
from fastapi_jwt_auth.exceptions import AuthJWTException
from main import get_db
from schemas import UserSignup, LoginModel, ProfileUpdate
from models import User, TokenBlacklist
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from sqlalchemy import or_

EXPIRATION_ACCESS_TOKEN = datetime.now() + timedelta(hours=1)
EXPIRATION_REFRESH_TOKEN = datetime.now() + timedelta(days=1)


auth_routers = APIRouter(
    prefix='/auth',
)


@auth_routers.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = generate_password_hash(user.password),
        is_active = True
    )
    db.add(new_user)
    db.commit()

    data = {
        'status': status.HTTP_201_CREATED,
        'message': 'User created successfully',
        'data': new_user
    }
    return jsonable_encoder(data)


@auth_routers.post("/login", status_code=200)
async def login(user: LoginModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(or_(User.username == user.email_username, User.email == user.email_username)).first()

    if db_user and check_password_hash(db_user.hashed_password, user.password):
        access_token = Authorize.create_access_token(subject = db_user.username, expires_time=EXPIRATION_ACCESS_TOKEN)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=EXPIRATION_REFRESH_TOKEN)

        data = {
            'message': 'Logged in successfully',
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return jsonable_encoder(data)
    raise HTTPException(status_code=400, detail="Incorrect username or password")


@auth_routers.get("/login/refresh")
async def refresh_token(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()

        current_user = Authorize.get_jwt_subject()

        db_user = db.query(User).filter(User.username == current_user).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        new_access_token = Authorize.create_access_token(subject = db_user.username, expires_time=EXPIRATION_ACCESS_TOKEN   )

        response_model = {
            'success': True,
            'code': 200,
            'message': "New access token is created",
            'data': {
                'access_token': new_access_token
            }
        }
        return response_model

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


@auth_routers.get("/profile", status = status.HTTP_200_OK)
async def profile(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

        user_db = db.query(User).filter(User.username == current_user).first()

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f"Error: {e} "
        )
    else:
        data = {
            'success': True,
            'message': 'Profile malumotlari',
            'email': user_db.email,
            'username': user_db.username
        }
        return jsonable_encoder(data, status = status.HTTP_200_OK)


@auth_routers.post("/update-profile")
async def update_profile(user: ProfileUpdate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        user_db = db.query(User).filter(User.username == current_user).first()
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f"Error: {e} "
        )
    else:
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user_db, key, value)

        db.commit()
        db.refresh(user_db)
        return user_db


@AuthJWT.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token, db: Session = Depends(get_db)):
    jti = decrypted_token["jti"]
    token = db.query(TokenBlacklist).filter(TokenBlacklist.jti == jti).first()
    return token is not None


@auth_routers.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    try:
        Authorize.jwt_required()

        jti = Authorize.get_raw_jwt()["jti"]

        blacklisted_token = TokenBlacklist(jti=jti)
        db.add(blacklisted_token)
        db.commit()

        return {
            "success": True,
            "message": "Access token revoked. Logged out successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

