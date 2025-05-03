from duckduckgo_search import DDGS

def retrieve_marketing_info(query: str) -> list[str]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=2):
            results.append(r["body"])
    return results
