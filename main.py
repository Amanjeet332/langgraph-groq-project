from app.graph import get_graph
from langchain_core.messages import HumanMessage
import os

graph = get_graph()

if __name__ == "__main__":
    result = graph.invoke({"messages": [HumanMessage(content="What is 6 times 7?")]})

    for msg in result["messages"]:
        print(f"{msg.type.upper()}: {msg.content}")

    # Optional: print trace URL (only works if tracing is enabled)
    run_id = result.get("run_id")
    if run_id:
        print(
            f"\n🔎 View trace on LangSmith:\nhttps://smith.langchain.com/public/{run_id}"
        )
    else:
        print("\nℹ️ No run_id found. Make sure LANGSMITH_TRACING=true is set.")
