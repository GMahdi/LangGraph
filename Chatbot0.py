from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model='gpt-4')

def process_message(state: AgentState) -> AgentState:
    """Process input message"""
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(response.content)
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process_message)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()

conversation_history = []
user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = app.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter: ")
