# agent.py
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from my_llm_module import ChatTavily  # Your Tavily client module
from my_db_module import execute_query  # Contains your execute_query() function
from dotenv import load_dotenv
import os

# Load environment variables (including TAVILY_API_KEY)
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY", "your_api_key")

# Instantiate your Tavily client.
tavily_llm = ChatTavily(model="tavily-1.0", api_key=tavily_api_key)

# Node functions for the workflow.
def input_node(state):
    return state

def query_gen_node(state):
    user_query = state.get("user_query", "")
    sql_query = tavily_llm.generate(user_query)
    state["sql_query"] = sql_query
    state["messages"].append(AIMessage(content=f"Generated SQL Query: {sql_query}"))
    return state

def execute_query_node(state):
    sql_query = state.get("sql_query", "")
    #print(f"SQL QUERY:"{sql_query})
    result = execute_query(sql_query)
    state["result"] = result
    state["messages"].append(ToolMessage(content=f"Query Result: {result}", tool_call_id="execute_query_dummy"))
    return state

def output_node(state):
    final_answer = f"SQL Query: {state.get('sql_query')}\nResult: {state.get('result')}"
    state["final_answer"] = final_answer
    state["messages"].append(HumanMessage(content=final_answer))
    return state

# Build the workflow graph.
workflow = StateGraph(dict)
workflow.add_node("input_node", input_node)
workflow.add_node("query_gen_node", query_gen_node)
workflow.add_node("execute_query_node", execute_query_node)
workflow.add_node("output_node", output_node)

# Link nodes: input -> query generation -> execution -> output.
workflow.add_edge(START, "input_node")
workflow.add_edge("input_node", "query_gen_node")
workflow.add_edge("query_gen_node", "execute_query_node")
workflow.add_edge("execute_query_node", "output_node")
workflow.add_edge("output_node", END)

app = workflow.compile()

# Shortened prompt (under 400 characters).
initial_state = {
    "user_query": (
        "Return a valid SQL query to compute average salary by title. "
        "Schema: employees(emp_no, emp_title_id); salaries(salary, emp_no); titles(title_id, title). "
        "Join employees to salaries on emp_no and to titles on emp_title_id=title_id. "
        "Group by titles.title. Query must start with SELECT and end with ;."
    ),
    "messages": []
}

final_state = app.invoke(initial_state)
print(final_state["final_answer"])
