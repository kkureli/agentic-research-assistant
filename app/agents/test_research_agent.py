from app.agents.research_agent import run_research_agent


TEST_QUESTIONS = [
    # Sufficient internal evidence
    "What was Asteria Cloud Systems' revenue growth in Q2 2026?",
    # Multi-entity comparison
    "Compare the main causes of growth slowdown at Asteria and Nova.",
    # Retrieval + calculation
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
        print("CRITIC TRACE:")
        for critic_trace in result.critic_traces:
            print(
                f"Round {critic_trace.round} | "
                f"Sufficient: {critic_trace.sufficient} | "
                f"Issues: {critic_trace.issues} | "
                f"Follow-up: {critic_trace.follow_up_query}"
            )
        print(f"Research LLM calls: {result.llm_call_count}")
        print(f"Critic LLM calls: {result.critic_llm_call_count}")

        print()
