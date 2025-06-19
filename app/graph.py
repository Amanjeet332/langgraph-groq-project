# app/graph.py
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage

def echo_node(state):
    user_msg = state["messages"][-1].content
    return {"messages": [AIMessage(content=f"You said: {user_msg}")]}

def get_graph():
    from langgraph.graph.message import add_messages

    builder = StateGraph()
    builder.add_node("echo", echo_node)
    builder.set_entry_point("echo")
    return builder.compile()
