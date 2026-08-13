import re

CITATION_PATTERN = re.compile(r"\[(S|W)(\d+)\]")


def extract_citations(text: str) -> list[str]:
    citations = [
        f"{prefix}{number}" for prefix, number in CITATION_PATTERN.findall(text)
    ]

    return list(dict.fromkeys(citations))
