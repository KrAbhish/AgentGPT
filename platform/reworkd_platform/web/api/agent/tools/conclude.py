from typing import Any

from fastapi.responses import StreamingResponse as FastAPIStreamingResponse

from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.tool import Tool
from loguru import logger
from reworkd_platform.web.api.agent.tools.utils import summarize

class Conclude(Tool):
    description = "Use when all the task in the objective"

    def summarize_results(self, results, goal, language):
        # text_tokens = self.token_service.tokenize("".join(results))
        # text = self.token_service.detokenize(text_tokens)
        text = "".join(results)
        logger.info(f"Summarizing text: {text}")

        return summarize(
            model=self.model,
            language=language,
            goal=goal,
            text=text,
        )

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        
        completed_tasks_results = args[-1]
        language = args[-2]
        logger.info(f"External arguments {args}")
        conclusion = self.summarize_results(completed_tasks_results, goal, language)
        return conclusion
