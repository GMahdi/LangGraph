from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from typing import List, Dict, TypedDict
import os
from dotenv import load_dotenv

load_dotenv()
class SimpleState(TypedDict):
    name: str
    message: str

def greetingNode(state: SimpleState) -> SimpleState:
    """Update the name and age of the user"""
    state["message"] = f"Hi, {state['name']}, how is life?"
    return state

graph0 = StateGraph(SimpleState)
graph0.add_node("update", greetingNode)

graph0.add_edge(START, "update")
graph0.add_edge("update", END)

app = graph0.compile()
print(app.invoke({"name": "Bidu", "age":60}))

png_data = app.get_graph().draw_mermaid_png()

with open("langgraph.png", "wb") as f:
    f.write(png_data)

print("Image saved to langgraph.png")






