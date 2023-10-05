from dotenv import load_dotenv
import os
import weaviate
import json
from schema import startupSchema

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

file_path = str(os.getenv("JSON_DATA")) + "/GenAIstartups.json"
print (file_path)
startUp = startupSchema.startupSchema(file_path)
json_data = startUp.read_json()

if json_data:
    print(f"...Weaviate DB in construction...")
    startUp.startupSchemaCreate(client)
    print(f"...DB Created...")
    print(f"...upload data...")
    startUp.startupSchemaFeed(json_data, client)
    print(f"...  ...")
    print(f"... Data Upload Complete ...")
