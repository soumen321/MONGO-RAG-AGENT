# Graph Module
# Defines the graph state, agent nodes, and graph initialization for the RAG workflow

from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.mongodb import MongoDBSaver
from typing_extensions import TypedDict

# Define the graph state type with messages that can accumulate
class GraphState(TypedDict):
    # Define a messages field that keeps track of conversation history
    messages: Annotated[list, add_messages]

def agent(state: GraphState, llm_with_tools) -> GraphState:
    """
    Agent node.

    Args:
        state (GraphState): The graph state.
        llm_with_tools: The LLM with tools.

    Returns:
        GraphState: The updated messages.
    """

    messages = state["messages"]

    result = llm_with_tools.invoke(messages)

    return {"messages": [result]}

def tool_node(state: GraphState, tools_by_name) -> GraphState:
    """
    Tool node.

    Args:
        state (GraphState): The graph state.
        tools_by_name (Dict[str, Callable]): The tools by name.

    Returns:
        GraphState: The updated messages.
    """
    result = []

    tool_calls = state["messages"][-1].tool_calls

    for tool_call in tool_calls:
        tool = tools_by_name[tool_call["name"]]

        observation = tool.invoke(tool_call["args"])

        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))

    return {"messages": result}

def route_tools(state: GraphState):
    """
    Route to the tool node if the last message has tool calls. Otherwise, route to the end.

    Args:
        state (GraphState): The graph state.

    Returns:
        str: The next node to route to.
    """
    messages = state.get("messages", [])

    if len(messages) > 0:
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"

    return END

def init_graph(llm_with_tools, tools_by_name, mongodb_client):
    """
    Initialize the graph.

    Args:
        llm_with_tools: The LLM with tools.
        tools_by_name (Dict[str, Callable]): The tools by name.
        mongodb_client (MongoClient): The MongoDB client.

    Returns:
        StateGraph: The compiled graph.
    """
    graph = StateGraph(GraphState)

    graph.add_node("agent", lambda state: agent(state, llm_with_tools))

    graph.add_node("tools", lambda state: tool_node(state, tools_by_name))

    graph.add_edge(START, "agent")

    graph.add_edge("tools", "agent")

    graph.add_conditional_edges("agent", route_tools, {"tools": "tools", END: END})

    checkpointer = MongoDBSaver(mongodb_client)

    return graph.compile(checkpointer=checkpointer)

def execute_graph(app, thread_id: str, user_input: str) -> None:
    """
    Stream outputs from the graph.

    Args:
        app: The compiled graph application.
        thread_id (str): The thread ID.
        user_input (str): The user's input.
    """
    input = {"messages": [("user", user_input)]}

    config = {"configurable": {"thread_id": thread_id}}

    for output in app.stream(input, config):
        for key, value in output.items():
            print(f"Node {key}:")
            print(value)

    print("---FINAL ANSWER---")

    print(value["messages"][-1].content)