from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.connection import get_session
from app.schemas import (

    GroupCreateRequest, GroupBaseScheme, ParticipantCreateRequest, ParticipantBaseScheme, GroupScheme,
    ParticipantScheme)
from app.utils import promotion as utils


api_router = APIRouter(
    prefix="",
    tags=["Group"],
)


@api_router.post(
    "/group",
    status_code=status.HTTP_201_CREATED,
    responses={},
)
async def create_group(
    _: Request,
    group_instance: GroupCreateRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    promotion = await utils.create_group(session, group_instance)
    return GroupBaseScheme.from_orm(promotion).id


@api_router.get(
    "/groups",
    status_code=status.HTTP_200_OK,
    response_model=list[GroupBaseScheme],
    responses={},
)
async def get_groups(
    _: Request,
    session: AsyncSession = Depends(get_session),
):
    groups = await utils.get_groups(session)

    return [GroupBaseScheme.from_orm(group) for group in groups]


@api_router.get(
    "/group/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=GroupScheme,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def get_group(
    _: Request,
    group_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
):
    group = await utils.get_group(session, group_id)
    if group:
        return GroupScheme.from_orm(group)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )


@api_router.put(
    "/group/{group_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def update_promotion(
    _: Request,
    group_id: int = Path(...),
    group_instance: GroupCreateRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):

    updated = await utils.update_group(session, group_id, group_instance)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )


@api_router.delete(
    "/group/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def delete_promotion(
    _: Request,
    group_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
):
    deleted = await utils.delete_group(session, group_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )


@api_router.post(
    "group/{group_id}/participant/",
    status_code=status.HTTP_201_CREATED,
)
async def create_participant(
    _: Request,
    group_id: int = Path(...),
    participant_instance: ParticipantCreateRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    participant = await utils.create_participant(session, group_id, participant_instance)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return ParticipantBaseScheme.from_orm(participant).id


@api_router.delete(
    "/group/{group_id}/participant/{participant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def delete_member(
    _: Request,
    group_id: int = Path(...),
    participant_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
):
    deleted = await utils.delete_participant(session, group_id, participant_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )


@api_router.post(
    "/group/{group_id}/toss",
    status_code=status.HTTP_200_OK,
    response_model=list[ParticipantScheme],
    responses={},
)
async def toss(
    _: Request,
    group_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
):
    participants = await utils.create_toss(session, group_id)
    return [ParticipantScheme.from_orm(participant) for participant in participants]


@api_router.get(
    "/group/{group_id}/participant/{participant_id}/recipient",
    status_code=status.HTTP_200_OK,
    response_model=ParticipantBaseScheme,
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def get_group(
    _: Request,
    group_id: int = Path(...),
    participant_id: int = Path(...),
    session: AsyncSession = Depends(get_session),
):
    recipient = await utils.get_recipient(session, group_id, participant_id)
    if recipient:
        return ParticipantBaseScheme.from_orm(recipient)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
