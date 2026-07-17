from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.application.services.user import UserService
from app.presentation.http.v1.deps.user import get_user_service
from app.presentation.http.v1.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service)
):
    return await service.get_user(user_id)
