from typing import TypeVar

from fastapi import Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from reworkd_platform.db.crud.agent import AgentCRUD
from reworkd_platform.db.dependencies import get_db_session
from reworkd_platform.schemas.agent import (
    AgentChat,
    AgentRun,
    AgentRunCreate,
    AgentSummarize,
    AgentTaskAnalyze,
    AgentTaskCreate,
    AgentTaskExecute,
    Loop_Step,
)
from reworkd_platform.schemas.user import UserBase
from reworkd_platform.settings import settings
from reworkd_platform.web.api.dependencies import get_current_user
from loguru import logger

T = TypeVar(
    "T", AgentTaskAnalyze, AgentTaskExecute, AgentTaskCreate, AgentSummarize, AgentChat
)


def agent_crud(
    user: UserBase = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> AgentCRUD:
    agent_crud_obj = AgentCRUD(session, user)
    logger.info(f"Agent crud {agent_crud_obj} with user {user} and sessions")
    return agent_crud_obj


async def agent_start_validator(
    
    body: AgentRunCreate = Body(
        example={
            "goal": "Create business plan for a bagel company",
            "modelSettings": {
                "customModelName": settings.azure_openai_deployment_name,
            },
        },
    ),
    crud: AgentCRUD = Depends(agent_crud),
) -> AgentRun:
    logger.info(f"Running agent_start_validator with body {body} and agent crud {crud}")
    id_ = (await crud.create_run(body.goal)).id
    logger.info(f"Agent run id {id_}")
    agent_run = AgentRun(**body.dict(), run_id=str(id_))
    logger.info(f"AgentRun: {agent_run}")
    return agent_run


async def validate(body: T, crud: AgentCRUD, type_: Loop_Step) -> T:
    body.run_id = (await crud.create_task(body.run_id, type_)).id
    return body


async def agent_analyze_validator(
    body: AgentTaskAnalyze = Body(),
    crud: AgentCRUD = Depends(agent_crud),
) -> AgentTaskAnalyze:
    return await validate(body, crud, "analyze")


async def agent_execute_validator(
    body: AgentTaskExecute = Body(
        example={
            "goal": "Perform tasks accurately",
            "task": "Write code to make a platformer",
            "analysis": {
                "reasoning": "I like to write code.",
                "action": "code",
                "arg": "",
            },
        },
    ),
    crud: AgentCRUD = Depends(agent_crud),
) -> AgentTaskExecute:
    return await validate(body, crud, "execute")


async def agent_create_validator(
    body: AgentTaskCreate = Body(),
    crud: AgentCRUD = Depends(agent_crud),
) -> AgentTaskCreate:
    return await validate(body, crud, "create")


async def agent_summarize_validator(
    body: AgentSummarize = Body(),
    crud: AgentCRUD = Depends(agent_crud),
) -> AgentSummarize:
    return await validate(body, crud, "summarize")


async def agent_chat_validator(
    body: AgentChat = Body(),
    crud: AgentCRUD = Depends(agent_crud),
) -> AgentChat:
    return await validate(body, crud, "chat")
