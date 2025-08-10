"""Web Search Tool for Ollama integration using SearXNG."""

import httpx
from homeassistant.helpers.llm import Tool, ToolInput

SEARXNG_URL = "https://search.congeant.org/search"

class WebSearchTool(Tool):
    name = "web_search"
    description = "Search the web using SearXNG and return the top results."
    parameters = {
        "query": {
            "type": "string",
            "description": "Search query to look up on the web."
        }
    }

    async def call(self, tool_input: ToolInput) -> str:
        query = tool_input.args.get("query")
        if not query:
            return "No query provided."
        params = {
            "q": query,
            "format": "json",
            "categories": "general"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(SEARXNG_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])
                if not results:
                    return "No results found."
                # Return top 3 results as a summary
                summary = "\n".join([
                    f"{r.get('title')}: {r.get('url')}\n{r.get('content','')}" for r in results[:3]
                ])
                return summary
            except Exception as e:
                return f"Web search failed: {e}"
