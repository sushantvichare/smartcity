from agent import SmartCityAgent


def main():
    print("=" * 60)
    print("Mumbai Smart City AI Assistant")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    agent = SmartCityAgent()

    while True:
        try:
            query = input("\nYou: ").strip()

            if not query:
                continue

            if query.lower() in ["exit", "quit"]:
                print("Assistant: Goodbye!")
                break

            result = agent.run_agent(query)

            print("\nAssistant:")

            if isinstance(result, dict):

                if result.get("success"):
                    print(result.get("answer", "No answer generated."))

                else:
                    print(
                        result.get(
                            "answer",
                            result.get("error", "Something went wrong.")
                        )
                    )

            else:
                print(result)

        except KeyboardInterrupt:
            print("\n\nAssistant: Goodbye!")
            break

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()