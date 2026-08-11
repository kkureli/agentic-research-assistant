COMPANY_ALIASES = {
    "asteria": "asteria_cloud",
    "asteria cloud": "asteria_cloud",
    "asteria cloud systems": "asteria_cloud",
    "nova": "nova_mobility",
    "nova mobility": "nova_mobility",
}


def resolve_company(company_query: str | None) -> str | None:
    if company_query is None:
        return None

    normalized = company_query.strip().lower()

    return COMPANY_ALIASES.get(normalized)
