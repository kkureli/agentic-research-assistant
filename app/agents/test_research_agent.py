from app.agents.research_agent import run_research_agent


TEST_QUESTIONS = [
    # Internal KB
    "Why did Asteria's revenue growth slow down in Q2 2026?",
    # Multi-entity + calculation
    (
        "What was Asteria's revenue growth in Q2 2026 and "
        "Nova's revenue growth in Q2 2026? "
        "Calculate the percentage-point difference."
    ),
    # Public web
    "When was Galatasaray founded?",
    # Insufficient internal evidence
    "What was Nova Mobility's employee headcount in Q2 2026?",
]


if __name__ == "__main__":
    for question in TEST_QUESTIONS:
        print("=" * 100)
        print(f"QUESTION: {question}")
        print()

        result = run_research_agent(question)

        print("ANSWER:")
        print(result.answer)
        print()

        print("TRACE:")
        for trace in result.traces:
            print(
                f"Step {trace.step} | "
                f"Tool: {trace.tool_name} | "
                f"Arguments: {trace.arguments}"
            )

        print()
