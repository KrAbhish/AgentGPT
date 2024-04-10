from typing import Any
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain import SQLDatabase
from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.settings import settings
from loguru import logger
from reworkd_platform.web.api.agent.tools.tool import Tool
from reworkd_platform.web.api.agent.prompts import (SQL_PREFIX)

top_k = 10
res_format = 'markdown'



# Create agents required to get the insights 








class SalesDatabaseSql(Tool):
    description = (
       "Can be used to answer questions which are fact based such as contact details, names, id, status,etc along with information about opportunities, their winning probablity or does have a specific answers which can be retrieved from the SQL tables. This can also be used to get/retrieve information about customers, consignees such as shipments done by customers, customer sales, total values of customer, total logistics spend. SQL data retrieval queries seek specific information from a database. Users often inquire about finding, filtering, or displaying data, such as retrieving customer details, product information, or sales records that meet certain criteria. These queries can involve single or multiple tables and commonly use clauses like SELECT, WHERE, JOIN, and GROUP BY to tailor the output to their needs"
    )
    public_description = "Interact with database with information about potential customers. "
    # arg_description = "The query argument to search for. This value is always populated and cannot be an empty string."
    db_password = settings.postgres_password
    db_username = settings.postgres_username
    db_server = settings.postgres_server

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        logger.info(f"Running tool SalesDatabaseSql with task {task}")
        # chain = LLMChain(llm=self.model, prompt=execute_task_prompt)
        completed_tasks_results = args[-1]
        logger.info(f"External arguments {args}")
        output = self.agent_sales_sql_fn(task, completed_tasks_results)
        logger.info(f"Response of the SalesDatabaseSql {output}")
        # return FastAPIStreamingResponse(output['output'])
        return stream_string(output['output'])
    
    def agent_sales_sql_fn(self, task, completed_tasks_results):
        question_prompt=[
            {"role": "system", "content": "Assistant is an agent designed to interact with a PostGres SQL database. Firstly list the tables and Get schema of the table."},
            {"role": "system", "content": f"{SQL_PREFIX.format(top_k, res_format)}"},
            {"role": "user", "content": f"Following is the {task} and here are the results from the previous tasks: {completed_tasks_results} to reference from."},
            ]
        agent_sales_sql = self.get_sales_sql_agent()
        result = agent_sales_sql(question_prompt)
        return result 
    
    # # Connecting to Postgres and restricting to 1 table
    def connect_db(self):
        
        db = SQLDatabase.from_uri("postgresql://"+SalesDatabaseSql.db_username+":"+SalesDatabaseSql.db_password + SalesDatabaseSql.db_server,
                            schema="sales_copilot")
        return db
    
    def get_sales_sql_agent(self): 
        #Azure Postgres Read only DB credentials
       
        logger.info("Trying to establish connection to postgresDB")
        db = self.connect_db()
        logger.info("Connection to postgresDB successfully established")
        toolkit = SQLDatabaseToolkit(db=db, llm=self.model)
        logger.info("Initialized SQLDatabaseToolkit")
        sales_agent = create_sql_agent(
        llm=self.model,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        # prefix = SQL_PREFIX,
        # suffix = SQL_SUFFIX,
        agent_executor_kwargs={"return_intermediate_steps":True}
        )
        logger.info("Initialized Sales SQL agent")
        return sales_agent


   