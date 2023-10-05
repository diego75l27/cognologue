from dotenv import load_dotenv
import os
import weaviate

# load environment variables from .env.list
load_dotenv()

open_ai_key = os.getenv("OPENAI_API_KEY")
client = weaviate.Client(
    url = "http://localhost:8081",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key=""),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-OpenAI-Api-Key": open_ai_key  # Replace with your inference API key
    }
)


client.schema.delete_class("StartupUserCase")
