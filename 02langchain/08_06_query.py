import os

from dotenv import load_dotenv
from langchain_classic  import hub
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.runnables import RunnablePassthrough
from langchain_deepseek import ChatDeepSeek
from typing_extensions import Annotated
from typing_extensions import TypedDict

load_dotenv()

db = SQLDatabase.from_uri("sqlite:///08/Chinook.db")
print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM Artist LIMIT 10;")

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

query_prompt_template.messages[0].pretty_print()

llm = ChatDeepSeek(
    model = "deepseek-v3",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    api_base=os.environ.get("OPENAI_API_BASE")
)

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

def write_query(state: State):
    """Generate SQL query to fetch information"""
    prompt = query_prompt_template.invoke({
        "dialect": db.dialect,
        "top_k": 10,
        "table_info": db.get_table_info(),
        "input": state["question"]
    })
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

sqlMessage = write_query({"question": "一共有多少个员工？"})
print(sqlMessage)

def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

def answer_question(state: State):
    """Format answer based on the query result."""
    prompt = f"""Based on the SQL query:
{state["query"]}

And the query result:
{state["result"]}

Answer the user's question: {state["question"]}
Provide a concise and informative response.
"""
    return {"answer": llm.invoke(prompt).content}

sql_chain = (
    RunnablePassthrough.assign(query=write_query)
        .assign(result=execute_query)
        .assign(answer=answer_question)
)

question = "获取销售额最高的5为员工及其销售总额"
response = sql_chain.invoke({"question": question})

print("Question:", question)
print("\nGenerated SQL:")
print(response["query"])
print("\nExecution Result:")
print(response["result"])
print("\nAnswer:")
print(response["answer"])









