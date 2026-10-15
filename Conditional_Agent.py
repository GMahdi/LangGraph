from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict

class AgentState(TypedDict):
    num1: int
    operator1: str
    num2: int
    result1: int

    num3: int
    operator2: str
    num4: int
    result2: int

def add_oper1(state: AgentState) -> AgentState:
    """Addition operation function"""
    state["result1"] = state["num1"] + state["num2"]
    return state

def sub_oper1(state: AgentState) -> AgentState:
    """Subtraction operation function"""
    state["result1"] = state["num1"] - state["num2"]
    return state

def decide_next1(state: AgentState) -> AgentState:
    """Helps in deciding what to do next"""
    if state["operator1"] == "+":
        return "addition1"
    elif state["operator1"] == "-":
        return "subtraction1"

def add_oper2(state: AgentState) -> AgentState:
    """Addition operation function"""
    state["result2"] = state["num3"] + state["num4"]
    return state

def sub_oper2(state: AgentState) -> AgentState:
    """Subtraction operation function"""
    state["result2"] = state["num3"] - state["num4"]
    return state

def decide_next2(state: AgentState) -> AgentState:
    """Helps in deciding what to do next"""
    if state["operator2"] == "+":
        return "addition2"
    elif state["operator2"] == "-":
        return "subtraction2"

graph = StateGraph(AgentState)

graph.add_node("add1", add_oper1)
graph.add_node("sub1", sub_oper1)
graph.add_node("router1", lambda state: state)

graph.add_node("add2", add_oper2)
graph.add_node("sub2", sub_oper2)
graph.add_node("router2", lambda state: state)

graph.add_edge(START, "router1" )
graph.add_conditional_edges("router1",decide_next1,
                            {"addition1": "add1",
                             "subtraction1": "sub1" })
graph.add_edge("add1", "router2")
graph.add_edge("sub1", "router2")

graph.add_conditional_edges("router2",decide_next2,
                            {"addition2": "add2",
                             "subtraction2": "sub2" })
graph.add_edge("add2", END)
graph.add_edge("sub2", END)

app = graph.compile()
png_data = app.get_graph().draw_mermaid_png()

with open("langgraph.png", "wb") as f:
    f.write(png_data)

print("Image saved to langgraph.png")

result = app.invoke({"num1": 15, "num2": 25, "operator1": "+", "num3": 5, "num4": 25, "operator2": "-"})
print(result)


