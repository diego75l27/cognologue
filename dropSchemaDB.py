from dotenv import load_dotenv
import os
import weaviate

# load environment variables from .env.list
load_dotenv()

open_ai_key = os.getenv("OPENAI_API_KEY")
weaviate_url = os.getenv("WEAVIATE_API_URL")
weaviate_ai_key = os.getenv("WEAVIATE_API_KEY")

client = weaviate.Client(
    url = weaviate_url,  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_ai_key),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-OpenAI-Api-Key": open_ai_key  # Replace with your inference API key
    }
)



client.schema.delete_class("StartupUserCase")
