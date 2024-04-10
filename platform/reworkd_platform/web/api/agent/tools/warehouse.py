import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from typing import Any
from loguru import logger
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.tool import Tool
from reworkd_platform.settings import settings
from reworkd_platform.web.api.agent.prompts import external_data_prompt




    

class Warehouse(Tool):
    description = (
       "use this tool to do comparative insights on warehouse financial, capacity and operational metrics at site, region and Archetype level for every month. It can provide lowest performing regions, sites , areas for any metric like PDP, Unsold space, throughput, Capacity utilization or compare the change in any metrics value over months"
    )
    public_description = "Warehouse data"
    # arg_description = "The query argument to search for. This value is always populated and cannot be an empty string."

    def get_data(self):
        df=pd.read_csv(settings.warehouse_data_path)
        return df
    
    def get_warehouse_data_tool(self): 
        agent_warehouse_data = create_pandas_dataframe_agent(
            llm=self.model,
            df= self.get_data(),
            verbose=True )
        return agent_warehouse_data

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        logger.info(f"Running tool Warehouse with task {task}")
        # chain = LLMChain(llm=self.model, prompt=execute_task_prompt)

        completed_tasks_results = args[-1]
        logger.info(f"External arguments {args}")
        warehouse_data_tool = self.get_warehouse_data_tool()
        prompt = external_data_prompt.format_prompt(
            task=task,
            previous_results=completed_tasks_results,
        )
        output = {}
        output['output'] = warehouse_data_tool.run(prompt)
        logger.info(f"Response of the Warehouse {output}")
        # return FastAPIStreamingResponse(output['output'])
        return stream_string(output['output'])