"""Command-line entry point for the AI Tool-Using Agent."""

import uuid

from langchain_core.messages import HumanMessage, AIMessage

from agent_graph import invoke_agent
from memory_store import (
    initialize_memory,
    save_message,
    load_recent_messages,
    save_fact,
    search_facts,
)


def main():
    initialize_memory()

    session_id = input(
        "Session ID (press Enter for a new session): "
    ).strip()

    if not session_id:
        session_id = str(uuid.uuid4())

    print(f"\nAI Tool-Using Agent | session: {session_id}")
    print("Tools: calculator, time, web search, public API")
    print("Commands: /remember <fact>, /memory, /exit\n")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if text.lower() in {"/exit", "exit", "quit"}:
            print("Goodbye.")
            break

        if not text:
            continue

        if text.startswith("/remember "):
            fact = text[len("/remember "):].strip()

            if fact:
                save_fact(session_id, fact)
                print("Agent: Saved that fact to SQLite memory.\n")
            else:
                print("Agent: Please provide a fact to remember.\n")

            continue

        if text == "/memory":
            facts = search_facts(session_id)

            if facts:
                print(
                    "Agent:",
                    "\n".join(f"- {fact}" for fact in facts),
                    "\n",
                )
            else:
                print("Agent: No saved facts.\n")

            continue

        # Keep the original question unchanged.
        original_question = text

        # Load recent conversation history.
        history_rows = load_recent_messages(
            session_id,
            limit=10,
        )

        prior = []

        for role, content in history_rows:
            if role == "user":
                prior.append(HumanMessage(content=content))
            elif role == "assistant":
                prior.append(AIMessage(content=content))

        # Search for facts matching the question.
        facts = search_facts(
            session_id,
            query=original_question,
            limit=5,
        )

        # If there is no direct match, provide recent saved facts.
        if not facts:
            facts = search_facts(
                session_id,
                limit=5,
            )

        # Build the agent input.
        if facts:
            agent_input = (
                "Saved user facts:\n"
                + "\n".join(f"- {fact}" for fact in facts)
                + "\n\nUse these facts when relevant. "
                "If a saved fact directly answers the user's question, "
                "answer using that fact. Do not invent a different fact."
                + "\n\nUser question: "
                + original_question
            )
        else:
            agent_input = original_question

        # Save the original question to conversation history.
        save_message(
            session_id,
            "user",
            original_question,
        )

        try:
            _, answer = invoke_agent(
                agent_input,
                prior_messages=prior,
            )
        except Exception as exc:
            answer = (
                f"Agent error ({type(exc).__name__}): {exc}"
            )

        print(f"\nAgent: {answer}\n")

        save_message(
            session_id,
            "assistant",
            str(answer),
        )


if __name__ == "__main__":
    main()