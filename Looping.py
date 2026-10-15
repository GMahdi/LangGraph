from langgraph.graph import StateGraph, START, END
import random
from typing import List, TypedDict

class AgentState(TypedDict):
    lowest_val: int
    highest_val: int
    target: int
    guesses: List[int]
    counter: int

def init(state: AgentState) -> AgentState:
    """Initialize the agent state"""
    state["target"] = random.randint(1, 100)
    state["lowest_val"] = 0
    state["highest_val"] = 100
    state["counter"] = 1

def play(state: AgentState) -> AgentState:
    """Play the guessing game"""
   
    guess = random.randint( state["lowest_val"], state["highest_val"])
    state["guesses"].append(guess)
    state["counter"] += 1
    if guess > state["target"]:
        state["highest_val"] = state["target"]
    else:
        state["lowest_val"] = state["target"]
    return state

def to_continue(state: AgentState) -> AgentState:
    """Wether to contine to play the game"""
    if state["guesses"][-1] == state["target"]:
        print("Ho hah, you won the game")
        return "exit"
    if state["counter"] >= 7:
        print("Sorry you couldn't win the game")
        return "exit"
    else:
        print("Let's try one more time")
        return "loop"

graph = StateGraph(AgentState)
graph.add_node("init", init)
graph.add_node("play", play)
graph.add_node("to_continue", lambda x: x)

graph.add_edge(START, "init")
graph.add_edge("init", "play")
graph.add_conditional_edges("play",
                            to_continue,
                            {"loop": "play",
                             "exit": END})

app = graph.compile()
png_data = app.get_graph().draw_mermaid_png()

with open("langgraph.png", "wb") as f:
    f.write(png_data)

print("Image saved to langgraph.png")

agent = app.invoke({"lowest_val":0, "highest_val":500, "target":21, "guesses": [], "counter":-1})
print(agent)