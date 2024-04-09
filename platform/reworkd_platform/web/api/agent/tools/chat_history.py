from typing import Any, List
from loguru import logger
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from reworkd_platform.web.api.agent.tools.tool import Tool
from reworkd_platform.schemas.agent import AgentChat
from reworkd_platform.web.api.agent.dependancies import agent_chat_validator
from fastapi import Depends
from reworkd_platform.web.api.agent.prompts import chat_prompt
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.schema import HumanMessage
from lanarky.responses import StreamingResponse
from langchain import LLMChain
# from reworkd_platform.services.tokenizer.token_service import TokenService


def chat_history(llm_gpt, language, message: str, results: List[str]):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate(prompt=chat_prompt),
                *[HumanMessage(content=result) for result in results],
                HumanMessage(content=message),
            ]
        )
        logger.info(f"Chat: {prompt}")
        chain = LLMChain(llm=llm_gpt, prompt=prompt)

        return StreamingResponse.from_chain(
            chain,
            {"language": language},
            media_type="text/event-stream",
        )


class ChatHistory(Tool):
    description = (
        """ This tool should only be used when the current task is related to chat history or where the previous answers are referred or needed."""
    )
    public_description = "Chat History"
    # arg_description = "The query argument to search for. This value is always populated and cannot be an empty string."



    async def call(
        self, goal: str, task: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        completed_tasks_results = args[-1]
        logger.info(f"External arguments {args}")
        # chain = LLMChain(llm=self.model, prompt=execute_task_prompt)   
        logger.info(f"Chat with completed_tasks_results: {completed_tasks_results}")
        return chat_history( self.model, self.language, message = task, results = completed_tasks_results)
       