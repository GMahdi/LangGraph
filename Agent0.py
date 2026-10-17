from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from typing import List, TypedDict
from dotenv import load_dotenv
import os, random

load_dotenv()

class AgentState(TypedDict):
    messages : List[HumanMessage]

model = ChatOpenAI(model="gpt-4")

def processMessage(state: AgentState) -> AgentState:
    """Get response of the human message"""
    message = state["messages"]
    while message !="exit":
        response = model.invoke(state["messages"])
        print(response.content)
        message =  input("type 'exit' to finish or Enter: ")
        state["messages"] = state["messages"].append(message)
        
    return state

graph = StateGraph(AgentState)
graph.add_node("process", processMessage)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()

message = input("Enter: ")
app.invoke({"messages": message})
