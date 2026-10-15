from langgraph.graph import StateGraph, START, END
from typing import List, Dict, TypedDict

class AgentState(TypedDict):
    name: str
    nums: List[int]
    result: int
    operator: str

def process(state: AgentState) -> AgentState:
    """Process the input values"""
    print(f"Before action: {state}")
    if state["operator"] == "*":
        total = 1
        for n in state["nums"]:
            total *= n
    elif state["operator"] == "+":
        total = sum(state['nums'])
    else:
        print("Sorry can't process the operator, only + and * are allowed operators")
        state["result"] = f"Hi {state['name']}"
        return state
    state["result"] = f"Hi {state['name']}, the operation result of your numbers is {total}"
    print(f"After action: {state}")
    return state

myGraph = StateGraph(AgentState)

myGraph.add_node("process", process)

myGraph.add_edge(START, "process")
myGraph.add_edge("process", END)

app = myGraph.compile()

result = app.invoke({"name": "Mahdi", "operator": "/", "nums": [1,2,4,5]})
print(result["result"])