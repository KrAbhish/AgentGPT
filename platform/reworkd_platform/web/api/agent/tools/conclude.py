from typing import Any

from fastapi.responses import StreamingResponse as FastAPIStreamingResponse

from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.tool import Tool
from loguru import logger

class Conclude(Tool):
    description = "Use when all the task in the objective"

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        
        completed_tasks_results = args[-1]
        logger.info(f"External arguments {args}")
        output = self.agent_sales_sql_fn(task, completed_tasks_results)
        return stream_string("Task execution concluded.", delayed=True)
