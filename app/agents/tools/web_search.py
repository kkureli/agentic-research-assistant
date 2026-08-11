from tavily import TavilyClient

from app.core.config import settings

client = TavilyClient(api_key=settings.tavily_api_key)


def search_web(
    query: str,
    max_results: int = 5,
) -> str:
    response = client.search(
        query=query,
        max_results=max_results,
    )

    results = response.get("results", [])

    if not results:
        return "No web search results found."

    parts = []

    for index, result in enumerate(results, start=1):
        parts.append(
            f"[W{index}]\n"
            f"Title: {result.get('title', 'Unknown')}\n"
            f"URL: {result.get('url', '')}\n"
            f"Content: {result.get('content', '')}"
        )

    return "\n\n".join(parts)
