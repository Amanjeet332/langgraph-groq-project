from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()
os.environ["LANGSMITH_TRACING"] = "true"

# Set up in-memory checkpointer
memory = MemorySaver()

# Tool functions
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    return a * b

def divide(a: int, b: int) -> float:
    """Divide two numbers and return the result as float."""
    return a / b

tools = [add, multiply, divide]

# Define LLM and bind tools
llm = ChatOpenAI(
    model="llama3-70b-8192",
    openai_api_key="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",
    openai_api_base="https://api.groq.com/openai/v1"
)
llm_with_tools = llm.bind_tools(tools)

# System prompt
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# Assistant node logic
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build LangGraph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# ✅ Compile graph with memory checkpointer
graph = builder.compile()

# ✅ Optional: Pre-configured thread ID to persist memory
config = {"configurable": {"thread_id": "user-session-1"}}

# ✅ Optional: Sample run (you can remove this if importing the graph elsewhere)
if __name__ == "__main__":
    result = graph.invoke(
        {"messages": [{"role": "user", "content": "What is 5 + 7?"}]},
        config=config
    )
    print(result)
