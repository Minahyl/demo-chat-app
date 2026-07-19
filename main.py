import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    os.system("cls" if os.name == "nt" else "clear")

    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("API_Key")
    model = os.getenv("MODEL_DEPLOYMENT")

    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT is missing")

    if not api_key:
        raise ValueError("API_Key is missing")

    if not model:
        raise ValueError("MODEL_DEPLOYMENT is missing")

    # Create client
    client = OpenAI(
        base_url=endpoint,
        api_key=api_key,
    )

    print("=== Azure AI Chatbot ===")

    last_response_id = None

    while True:
        input_text = input("\nEnter a prompt (or type 'quit' to exit): ")

        if input_text.lower() == "quit":
            print("Goodbye!")
            break

        if not input_text.strip():
            print("Please enter a prompt.")
            continue

        # First request
        if last_response_id is None:
            response = client.responses.create(
                model=model,
                instructions="You are a helpful Python tutor. Explain concepts in English.",
                input=input_text,
            )
        # Continue conversation
        else:
            response = client.responses.create(
                model=model,
                instructions="You are a helpful Python tutor. Explain concepts in English.",
                input=input_text,
                previous_response_id=last_response_id,
            )

        print("\nResponse:")
        print(response.output_text)

        last_response_id = response.id


if __name__ == "__main__":
    main()