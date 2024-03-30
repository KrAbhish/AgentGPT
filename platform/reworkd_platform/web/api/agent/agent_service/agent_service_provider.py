from typing import Any, Callable, Coroutine, Optional

from fastapi import Depends

from reworkd_platform.db.crud.oauth import OAuthCrud
from reworkd_platform.schemas.agent import AgentRun, LLM_Model
from reworkd_platform.schemas.user import UserBase
from reworkd_platform.services.tokenizer.dependencies import get_token_service
from reworkd_platform.services.tokenizer.token_service import TokenService
from reworkd_platform.settings import settings
from reworkd_platform.web.api.agent.agent_service.agent_service import AgentService
from reworkd_platform.web.api.agent.agent_service.mock_agent_service import (
    MockAgentService,
)
from reworkd_platform.web.api.agent.agent_service.open_ai_agent_service import (
    OpenAIAgentService,
)
from reworkd_platform.web.api.agent.model_factory import create_model
from reworkd_platform.web.api.dependencies import get_current_user
from loguru import logger

def get_agent_service(
    validator: Callable[..., Coroutine[Any, Any, AgentRun]],
    streaming: bool = False,
    llm_model: Optional[LLM_Model] = None,
) -> Callable[..., AgentService]:
    def func(
        run: AgentRun = Depends(validator),
        user: UserBase = Depends(get_current_user),
        token_service: TokenService = Depends(get_token_service),
        oauth_crud: OAuthCrud = Depends(OAuthCrud.inject),
    ) -> AgentService:
        logger.info(f"Getting LLM service agent with AgentRun {run}, user {user}, token_service {token_service} and oauth_crud {oauth_crud}")
        if settings.ff_mock_mode_enabled:
            return MockAgentService()

        logger.info(f"Model settings {run.model_settings}")
        model = create_model(
            settings,
            run.model_settings,
            user,
            streaming=streaming,
            force_model=llm_model,
        )
        logger.info(f"Model: {model}")

        open_ai_agent_service = OpenAIAgentService(
            model,
            run.model_settings,
            token_service,
            callbacks=None,
            user=user,
            oauth_crud=oauth_crud,
        )
        logger.info(f"Openai agent service {open_ai_agent_service}")
        return open_ai_agent_service

    return func
