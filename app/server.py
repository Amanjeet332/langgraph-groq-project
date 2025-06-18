# app/server.py
from fastapi import FastAPI
from langserve import add_routes
from app.graph import get_graph

# Create your graph instance
graph = get_graph()

# Create FastAPI app
app = FastAPI()

# Add LangServe routes
add_routes(
    app,
    graph,
    path="/graph",
    enable_feedback_endpoint=True  # Optional
)
