from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, ToolMessage, BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

document_content = []

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content: str) -> str:
    """Updte the document with given content parameter"""
    global document_content
    document_content = content
    return f"Document has been successsfuly updated; the current content is: {document_content}"


@tool
def save(filename: str) -> str:
    """The function is used to save the draft copy in txt file"""
    if not filename.endswith('.txt'):
        filename = filename +'.txt'
    try:
        with open(filename, "w") as file:
            file.writable(document_content)
        print(f"The document has been saved to {filename}")
        return f"The document has been saved to {filename}"
    except Exception as e:
        return f"Error saving the document {filename}"

tools = [update, save]

model = ChatOpenAI(model='gpt-4o').bind_tools(tools)

def our_agent(state: AgentState) -> AgentState:
    """agent function for initializing system prompt"""
    system_prompt = SystemMessage(content=f"""
     You are a drafter, a helpful drafting assistant. You ae going to help the user update and modify documents.

     - If the user wants to update or modify conntnet, use the 'update' tool with the complete updated conent.
     - If the user wants to save and fonish, you need to use the 'save' tool.
     - Make usre to always show the current document state after modififcations. 

     The current document content is {document_content}
    """)

    if not state["messages"]:
        user_input = "I am ready to help you update the document. WHat you would like to create"
        user_message = HumanMessage(content=user_input)

    else:
        user_input = input("\nWhat would you like to do with the document?")
        print(f"\n USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    all_mesages = [system_prompt] + list(state["messages"]) + [user_message]

    response = model.invoke(all_mesages)

    print(f"\nAI: {response.content}")

    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"Using tools: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state['messages']) + [user_message, response]}


def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end the conversation"""

    messages = state["messages"]

    if not messages:
        return "continue"


    for message in reversed(messages):
        if (isinstance(message, ToolMessage)) and \
        "saved" in message.content.lower() and \
        "document" in message.contnet.lower():
            return "end"
    return "continue"


graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")
graph.add_edge("agent", "tools")

graph.add_conditional_edges("tools",
                            should_continue,
                            {
                                "continue": "agent",
                                "end": END
                            })

app = graph.compile()

def run_document_agent():
    print("\n ==== DRAFTER =====")
    state = {"messages": []}

    for step in app.stream(state, stream_mode='values'):
        if "messages" in step:
            print(step["messages"])

    print("\n ===  DRAFTER FINISHED ====")

if __name__ == '__main__':
    run_document_agent()