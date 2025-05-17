from __future__ import annotations

import argparse

from .agent import CasperAgent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Casper AI Agent")
    parser.add_argument("prompt", help="Prompt to send to the AI agent")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model")
    args = parser.parse_args(argv)

    agent = CasperAgent(model=args.model)
    try:
        response = agent.respond(args.prompt)
        print(response)
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
