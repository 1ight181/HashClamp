from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.application.cmd.create_user import CreateUserCommand
from app.application.cmd.update_user import UpdateUserCommand
from app.application.services.user import UserService

from app.presentation.http.v1.deps.user import get_user_service
from app.presentation.http.v1.schemas.user import UserResponse, UserCreateRequest, UserUpdateRequest

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


@router.post("", response_model=UserResponse)
async def create_user(
    user_create_req: UserCreateRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    cmd = CreateUserCommand(
        **user_create_req.model_dump(exclude_unset=True),
    )

    created_user = await service.create_user(cmd)

    return UserResponse.model_validate(created_user)

@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    user_id: UUID,
    user_update_req: UserUpdateRequest,
    service: UserService = Depends(get_user_service),
):
    cmd = UpdateUserCommand(
        changes=user_update_req.model_dump(exclude_unset=True),
    )

    await service.update_user(user_id, cmd)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
):
    await service.delete_user(user_id)
