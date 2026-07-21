import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
model_deployment = os.getenv("MODEL_DEPLOYMENT", "")
api_key = os.getenv("API_KEY", "")

if not model_deployment:
    raise ValueError("MODEL_DEPLOYMENT environment variable is not set")

if not api_key:
    raise ValueError("API_KEY environment variable is not set")


def web_search_tool():
    """
    This function demonstrates the usage of the Web Search Tool.
    It allows the user to perform multiple searches until they type
    'exit' or 'quit'.
    """

    # Clear the console
    os.system("cls" if os.name == "nt" else "clear")

    # Initialize OpenAI client
    client = OpenAI(
        base_url=azure_openai_endpoint,
        api_key=api_key
    )

    # Store conversation context
    last_response_id = None

    print("=" * 60)
    print("        🌐 AI Web Search Tool")
    print("Type 'exit' or 'quit' to close the application.")
    print("=" * 60)

    while True:

        # Get user query
        query = input("\nEnter your search query: ").strip()

        # Exit condition
        if query.lower() in ["exit", "quit"]:
            print("\nGoodbye! 👋")
            break

        # Empty input
        if not query:
            print("Please enter a valid search query.")
            continue

        print(f"\nSearching for: {query}\n")

        try:
            response = client.responses.create(
                model=model_deployment,
                instructions="""
You are an expert software engineer with extensive experience in Python,
JavaScript, TypeScript, C#, Java, SQL, cloud technologies, APIs,
and modern software architecture.

Always provide accurate, well-structured, and concise answers.
""",
                tools=[
                    {
                        "type": "web_search_preview"
                    }
                ],
                input=query,
                previous_response_id=last_response_id,
            )

            print("Response:\n")
            print(response.output_text)

            # Save conversation context
            last_response_id = response.id

        except Exception as ex:
            print(f"\nError: {ex}")


if __name__ == "__main__":
    web_search_tool()