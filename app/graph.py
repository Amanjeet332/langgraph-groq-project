# app/graph.py
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Tool definition
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

# LLM with tool bound
llm =ChatOpenAI(
    model="llama3-70b-8192",
    openai_api_key="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",
    openai_api_base="https://api.groq.com/openai/v1"
)
llm_with_tools = llm.bind_tools([multiply])


# llm = ChatOpenAI()
llm.invoke("Hello, world!")

# Tool-calling node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Define and compile the graph
def get_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode([multiply]))
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", END)
    return builder.compile()
