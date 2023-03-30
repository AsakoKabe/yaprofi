from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.models import Group, Participant
from app.schemas import (
    GroupCreateRequest, GroupBaseScheme, ParticipantCreateRequest)


async def create_group(
    session: AsyncSession,
    group_schema: GroupCreateRequest,
) -> Group:
    new_group = Group(
        name=group_schema.name,
        description=group_schema.description
    )

    session.add(new_group)
    await session.commit()
    await session.refresh(new_group)

    return new_group


async def get_groups(
    session: AsyncSession,
) -> list[GroupBaseScheme]:
    query = select(Group)
    groups = await session.scalars(query)

    return groups.all()


async def get_group(
    session: AsyncSession,
    group_id: int,
) -> Group | None:
    query = select(Group).where(Group.id == group_id)
    group = await session.scalar(query)
    if not group:
        return None

    for participant in group.participants:
        participant.recipient = await get_participant(session, participant.parent_id)

    return group


async def update_group(
    session: AsyncSession,
    group_id: int,
    group_instance: GroupCreateRequest,
) -> bool:
    if not await get_group(session, group_id):
        return False
    query = update(Group).where(Group.id == group_id).values(group_instance.dict())
    await session.execute(query)
    await session.commit()

    return True


async def delete_group(
    session: AsyncSession,
    group_id: int,
) -> bool:
    if not await get_group(session, group_id):
        return False
    query = delete(Group).where(Group.id == group_id)
    await session.execute(query)
    await session.commit()

    return True


async def create_participant(
    session: AsyncSession,
    group_id: int,
    participant_instance: ParticipantCreateRequest
) -> Participant | None:
    group = await get_group(session, group_id)

    if not group:
        return None

    new_participant = Participant(
        name=participant_instance.name,
        wish=participant_instance.wish,
    )

    session.add(new_participant)
    await session.commit()
    await session.refresh(new_participant)

    group.participants.append(new_participant)
    await session.commit()
    await session.refresh(group)

    return new_participant


async def get_participant(
    session: AsyncSession,
    participant_id: int,
) -> Participant | None:
    query = select(Participant).where(Participant.id == participant_id)
    participant = await session.scalar(query)
    if not participant:
        return None
    return participant


async def delete_participant(
    session: AsyncSession,
    group_id: int,
    participant_id: int,
) -> bool:
    group = await get_group(session, group_id)
    if not group:
        return False
    participant = await get_participant(session, participant_id)
    if not participant:
        return False
    query = delete(Participant).where(Participant.id == participant_id)
    await session.execute(query)
    await session.commit()

    return True


async def create_toss(
    session: AsyncSession,
    group_id: int,
):
    group = await get_group(session, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if len(group.participants) < 3:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
        )

    # 1 2 3
    # 3 1 2

    participants = group.participants
    for i in range(len(participants)):
        participants[i].recipient = participants[i - 1]
        group.participants[i].parent_id = participants[i-1].id

    # group.participants = participants
    await session.commit()
    await session.refresh(group)

    return group.participants


async def get_recipient(
    session: AsyncSession,
    group_id: int,
    participant_id: int,
) -> Participant | None:
    group = await get_group(session, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    participant = await get_participant(session, participant_id)
    if not participant:
        return False

    return await get_participant(session, participant.parent_id)
