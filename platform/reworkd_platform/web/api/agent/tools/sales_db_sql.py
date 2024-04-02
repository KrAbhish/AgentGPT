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
# # Connecting to Postgres and restricting to 1 table
def connect_db(db_password, db_username, db_server):
    db = SQLDatabase.from_uri("postgresql://"+db_username+":"+db_password+db_server,
                         schema="sales_copilot")
    return db


# Create agents required to get the insights 

def get_sales_sql_agent(llm_gpt): 
    #Azure Postgres Read only DB credentials
    db_password = settings.postgres_password
    db_username = settings.postgres_username
    db_server = settings.postgres_server
    logger.info("Trying to establish connection to postgresDB")
    db = connect_db(db_password, db_username,db_server)
    logger.info("Connection to postgresDB successfully established")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm_gpt)
    logger.info("Initialized SQLDatabaseToolkit")
    sales_agent = create_sql_agent(
    llm=llm_gpt,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # prefix = SQL_PREFIX,
    # suffix = SQL_SUFFIX,
    agent_executor_kwargs={"return_intermediate_steps":True}
    )
    logger.info("Initialized Sales SQL agent")
    return sales_agent




def agent_sales_sql_fn(task, llm):
    question_prompt=[
        {"role": "system", "content": "Assistant is an agent designed to interact with a PostGres SQL database. Firstly list the tables and Get schema of the table."},
        {"role": "system", "content": f"{SQL_PREFIX.format(top_k, res_format)}"},
        {"role": "user", "content": f"{task}"},
        ]
    agent_sales_sql = get_sales_sql_agent(llm)
    result = agent_sales_sql(question_prompt)
    return result 

class SalesDatabaseSql(Tool):
    description = (
       "Can be used to answer questions which are fact based such as contact details, names, id, status,etc along with information about opportunities, their winning probablity or does have a specific answers which can be retrieved from the SQL tables. This can also be used to get information about customers, consignees such as shipments done by customers, customer sales, total values of customer, total logistics spend. SQL data retrieval queries seek specific information from a database. Users often inquire about finding, filtering, or displaying data, such as retrieving customer details, product information, or sales records that meet certain criteria. These queries can involve single or multiple tables and commonly use clauses like SELECT, WHERE, JOIN, and GROUP BY to tailor the output to their needs"
    )
    public_description = "Interact with database with information about potential customers. "
    # arg_description = "The query argument to search for. This value is always populated and cannot be an empty string."

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        logger.info(f"Running tool SalesDatabaseSql with task {task}")
        # chain = LLMChain(llm=self.model, prompt=execute_task_prompt)
        output = agent_sales_sql_fn(task, self.model)
        logger.info(f"Response of the SalesDatabaseSql {output}")
        # return FastAPIStreamingResponse(output['output'])
        return stream_string(output['output'])


   