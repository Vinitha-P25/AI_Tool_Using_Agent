"""Tools available to the LangGraph agent."""
import math
import os
from datetime import datetime
from typing import Literal

import requests
from ddgs import DDGS
from langchain_core.tools import tool

@tool
def calculate(
    a: float,
    b: float,
    operation: Literal["add", "subtract", "multiply", "divide"]
) -> float:
    """Calculate using add, subtract, multiply, or divide."""
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("Numbers must be finite.")
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        result = a / b
    else:
        raise ValueError("Unsupported operation.")
    if not math.isfinite(result):
        raise ValueError("Result is not finite.")
    return result

@tool
def get_current_time() -> str:
    """Return the current local date and time with timezone."""
    return datetime.now().astimezone().isoformat(timespec="seconds")

@tool
def search_web(query: str) -> str:
    """Search the web and return a small set of result titles, descriptions, and URLs."""
    if not query.strip():
        return "Search query cannot be empty."
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query.strip(), max_results=5))
        if not results:
            return "No search results found."
        return "\n\n".join(
            f"Title: {r.get('title', 'No title')}\n"
            f"Description: {r.get('body', 'No description')}\n"
            f"URL: {r.get('href', 'No URL')}"
            for r in results
        )
    except Exception as exc:
        return f"Web search failed ({type(exc).__name__}): {exc}"

@tool
def get_public_api_data() -> str:
    """Get a random activity suggestion from a public activity API."""
    url = "https://bored-api.appbrewery.com/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return (
            f"Activity: {data.get('activity', 'Unknown')}\n"
            f"Type: {data.get('type', 'Unknown')}\n"
            f"Participants: {data.get('participants', 'Unknown')}"
        )
    except requests.RequestException as exc:
        return f"Public API request failed ({type(exc).__name__}): {exc}"
    except ValueError as exc:
        return f"Invalid API response: {exc}"

ALL_TOOLS = [calculate, get_current_time, search_web, get_public_api_data]
TOOL_MAP = {t.name: t for t in ALL_TOOLS}
