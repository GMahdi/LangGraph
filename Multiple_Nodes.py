from langgraph.graph import StateGraph
from typing import List, TypedDict

class AgentState(TypedDict):
    name: str
    age: int
    skills: List[str]
    final_output: str

def first_node(state: AgentState) -> AgentState:
    """This is the first node"""
    state["final_output"] = f"Hi {state['name']}"
    return state

def second_node(state: AgentState) -> AgentState:
    """This is the second node"""
    state["final_output"] = state["final_output"] + f", you are {state['age']} years old"
    return state

def third_node(state: AgentState) -> AgentState:
    """This is the third node"""
    state["final_output"] = state["final_output"] + f", you are expert in {state['skills']}"
    return state

graph = StateGraph(AgentState)
graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.add_node("third", third_node)
graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.add_edge("second", "third")
graph.set_finish_point("third")

app = graph.compile()

png_data = app.get_graph().draw_mermaid_png()

with open("langgraph.png", "wb") as f:
    f.write(png_data)

print("Image saved to langgraph.png")

result = app.invoke({"name": "Mahdi", "age": 40, "skills": ["AI", "ML", "Python"]})
print(result["final_output"])