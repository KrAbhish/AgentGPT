import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from typing import Any
from loguru import logger
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.tool import Tool
from reworkd_platform.settings import settings
from reworkd_platform.web.api.agent.prompts import external_data_prompt

def get_data():
    df=pd.read_csv(settings.ebit_region_data_path)
    return df

def get_warehouse_data_tool(llm_gpt): 
    agent_warehouse_data = create_pandas_dataframe_agent(
        llm=llm_gpt,
        df= get_data(),
        verbose=True )
    return agent_warehouse_data
    

class EBITWarehouse(Tool):
    description = (
       "This agent provides Warehouse EBIT at regional level for every month"
    )
    public_description = "Warehouse EBIT."
    # arg_description = "The query argument to search for. This value is always populated and cannot be an empty string."

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        logger.info(f"Running tool EBITWarehouse with task {task}")
        # chain = LLMChain(llm=self.model, prompt=execute_task_prompt)

        warehouse_data_tool = get_warehouse_data_tool(self.model)
        prompt = external_data_prompt.format_prompt(
            task=task,
        )
        output = {}
        output['output'] = warehouse_data_tool.run(prompt)
        logger.info(f"Response of the EBITWarehouse {output}")
        # return FastAPIStreamingResponse(output['output'])
        return stream_string(output['output'])