from typing import Annotated

from fastapi import Path, HTTPException, Query, APIRouter

from app.models.users import UserModel
from app.schemas.users import UserCreateRequest, UserUpdateRequest, UserSearchParams, UserResponse

user_router = APIRouter(prefix="/users", tags=["users"])


class UserModel:

    @staticmethod
    def get_hashed_password(password: str) ->str:
        """비밀번호 해시화"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def authenticate(cls, username: str, password: str) -> UserModel:
        for user in cls._data:
            if user.username == username and cls.verify_password(password, user.password):
                return user
        return None
@user_router.post('')
async def create_user(data: UserCreateRequest):
    user = UserModel(**data.model_dump())
    return user.id

@user_router.get('')
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404)
    return result

@user_router.get('/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users

@user_router.get('/{user_id}')
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.update(**data.model_dump())
    return user

@user_router.delete('/{user_id}')
async def delete_user(user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=404)
    user.delete()

    return {'detail': f'User {user_id}, Successfully Deleted'}

@user_router.post('/login', response_model=Token)
async def login_user(data: Annotated[OAuth2passwordRequestForm, Depends()]):
    user = UserModel.authenticate(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user_id": user.id})
    user.update(last_login=datetime.now())
    return Token(access_token=access_token, token_type="bearer")

@user_router.get('/me')
async def get_user(user: Annotated[UserModel, Depends(get_current_user)]):
    return user

@user_router.patch('/me')
async def update_user(
        user: Annotated[UserModel, Depends(get_current_user)],
        data: UserUpdateRequest,
):
    if user is None:
        raise HTTPException(statsu_code=404)
    user.update(**data.model_dump())
    return user

@user_router.delete('/me')
async def delete_user(user: Annotated[UserModel, Depends(get_current_user)]):
    user.delete()
    return {'datail': 'Successfully Deleted.'}

@user_router.post("/me/profile_image", status_code=200)
async def register_profile_image(image: UploadFile, user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    validate_image_extension(image)
    prev_image_url = user.profile_image_url
    try:
        image_url = await upload(image, "users/profile_images")
        user.profile_image_url = image_url
        await user.save()

        if prev_image_url is not None:
            delete_file(prev_image_url)

        return UserResponse(
            id=user.id,
            username=user.username,
            age=user.age,
            gender=user.gender,
            profile_image_url=user.profile_image_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error pccurred: {str(e)}")