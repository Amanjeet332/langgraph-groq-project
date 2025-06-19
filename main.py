# main.py
from fastapi import FastAPI
from langserve import add_routes
from app.graph import get_graph

app = FastAPI()

graph = get_graph()

# Serve the graph at root ("/")
add_routes(app, graph, path="/")
