from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, ToolMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add_operator(a: int, b: int) -> int:
    """Add operation for addition of two numbers"""
    return a + b

@tool
def sub_operator(a: int, b: int) -> int:
    """Minus operation for subtraction of two numbers"""
    return a - b

@tool
def multiply_operator(a: int, b: int) -> int:
    """Multiplication operation for two numbers"""
    return a * b

@tool
def div_operator(a: int, b: int) -> int:
    """Division operation for division of two numbers"""
    return a / b

tools = [add_operator, sub_operator, multiply_operator, div_operator]

model = ChatOpenAI(model='gpt-4').bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_message = """You are helpful assistant that helps in answering my queries"""
    response = model.invoke([system_message]+ state['messages'])
    return {"messages": response}

def should_continue(state: AgentState) -> AgentState:
    messages = state["messages"] 
    last_message = messages[-1]

    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point( "our_agent")
graph.add_conditional_edges("our_agent",
                            should_continue,
                            {"continue": "tools",
                             "end": END})
graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "add 3 + 4. Add 55 and 22; multiply the result with 5")]}
print_stream(app.stream(inputs, stream_mode="values"))

