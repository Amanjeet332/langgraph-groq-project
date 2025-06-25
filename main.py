# main.py
from fastapi import FastAPI
from langserve import add_routes
from app.graph import get_graph
import os, getpass
from dotenv import load_dotenv
app = FastAPI()

graph = get_graph()

load_dotenv()

add_routes(app, graph, path="/")
# _set_env("LANGSMITH_API_KEY")
print("LangSmith Tracing:", os.getenv("LANGSMITH_TRACING"))
print("LangSmith API Key:", os.getenv("LANGSMITH_API_KEY"))