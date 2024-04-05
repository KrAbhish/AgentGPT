from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from pydantic import BaseModel
from loguru import logger

from reworkd_platform.schemas.agent import (
    AgentChat,
    AgentRun,
    AgentSummarize,
    AgentTaskAnalyze,
    AgentTaskCreate,
    AgentTaskExecute,
    NewTasksResponse,
)
from reworkd_platform.web.api.agent.agent_service.agent_service import AgentService
from reworkd_platform.web.api.agent.agent_service.agent_service_provider import (
    get_agent_service,
)
from reworkd_platform.web.api.agent.analysis import Analysis
from reworkd_platform.web.api.agent.dependancies import (
    agent_analyze_validator,
    agent_chat_validator,
    agent_create_validator,
    agent_execute_validator,
    agent_start_validator,
    agent_summarize_validator,
)
from reworkd_platform.web.api.agent.tools.tools import get_external_tools, get_tool_name
from reworkd_platform.schemas.agent import ModelSettings
router = APIRouter()


modelSettings = ModelSettings()
@router.post(
    "/start",
)
async def start_tasks(
    req_body: AgentRun = Depends(agent_start_validator),
    agent_service: AgentService = Depends(get_agent_service(agent_start_validator)),
) -> NewTasksResponse:
    logger.info(f"Starting agent run")
    new_tasks = await agent_service.start_goal_agent(goal=req_body.goal)
    logger.info(f"Initializing new tasks {new_tasks}")
    return NewTasksResponse(newTasks=new_tasks, run_id=req_body.run_id)


@router.post("/analyze")
async def analyze_tasks(
    req_body: AgentTaskAnalyze = Depends(agent_analyze_validator),
    agent_service: AgentService = Depends(get_agent_service(agent_analyze_validator)),
) -> Analysis:
    logger.info(f"Analyze tasks")
    return await agent_service.analyze_task_agent(
        goal=req_body.goal,
        task=req_body.task or "",
        tool_names=req_body.tool_names or [],
    )


@router.post("/execute")
async def execute_tasks(
    req_body: AgentTaskExecute = Depends(agent_execute_validator),
    agent_service: AgentService = Depends(
        get_agent_service(validator=agent_execute_validator, streaming=True),
    ),
    # results:  AgentSummarize = Depends(agent_summarize_validator),
    # results: AgentChat = Depends(agent_chat_validator),

) -> FastAPIStreamingResponse:
    logger.info(f"Task execution {req_body.results}")
    # logger.info(f"Task execution, previous results {results}")
    return await agent_service.execute_task_agent(
        goal=req_body.goal or "",
        task=req_body.task or "",
        analysis=req_body.analysis or Analysis(),
        results=req_body.results or [],
    )


@router.post("/create")
async def create_tasks(
    req_body: AgentTaskCreate = Depends(agent_create_validator),
    agent_service: AgentService = Depends(get_agent_service(agent_create_validator)),
) -> NewTasksResponse:
    logger.info(f"Task creation initialized {req_body}")
    new_tasks = await agent_service.create_tasks_agent(
        goal=req_body.goal,
        tasks=req_body.tasks or [],
        last_task=req_body.last_task or "",
        result=req_body.result or "",
        completed_tasks=req_body.completed_tasks or [],
    )
    logger.info(f"Created tasks {new_tasks}")
    return NewTasksResponse(newTasks=new_tasks, run_id=req_body.run_id)


@router.post("/summarize")
async def summarize(
    req_body: AgentSummarize = Depends(agent_summarize_validator),
    agent_service: AgentService = Depends(
        get_agent_service(
            validator=agent_summarize_validator,
            streaming=True,
            llm_model=modelSettings.model,
        ),
    ),
) -> FastAPIStreamingResponse:
    logger.info(f"Summarization: req_body {req_body}")
    # logger.info(f"Summarization")
    return await agent_service.summarize_task_agent(
        goal=req_body.goal or "",
        results=req_body.results,
    )


@router.post("/chat")
async def chat(
    req_body: AgentChat = Depends(agent_chat_validator),
    agent_service: AgentService = Depends(
        get_agent_service(
            validator=agent_chat_validator,
            streaming=True,
            llm_model=modelSettings.model,
        ),
    ),
) -> FastAPIStreamingResponse:
    logger.info(f"Chat endpoint")
    logger.info(f"Chat: {req_body}")
    return await agent_service.chat(
        message=req_body.message,
        results=req_body.results,
    )


class ToolModel(BaseModel):
    name: str
    description: str
    color: str
    image_url: Optional[str]


class ToolsResponse(BaseModel):
    tools: List[ToolModel]


@router.get("/tools")
async def get_user_tools() -> ToolsResponse:
    logger.info(f"Getting available tools")
    tools = get_external_tools()
    logger.info(f"Following are the available tools {tools}")
    formatted_tools = [
        ToolModel(
            name=get_tool_name(tool),
            description=tool.public_description,
            color="TODO: Change to image of tool",
            image_url=tool.image_url,
        )
        for tool in tools
        if tool.available()
    ]

    return ToolsResponse(tools=formatted_tools)
