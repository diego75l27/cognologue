import json
import requests


class startupSchema:
    def __init__(self, file_path):
        self.file_path = file_path
        self.class_obj = {
            "class": "StartupUserCase",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text"
                },
                "generative-openai": {
                },
                "properties": [
                    {
                        "name": "idStartup",
                        "dataType": ["int"]
                    },
                    {
                        "name": "category",
                        "dataType": ["text"]
                    },
                    {
                        "name": "name",
                        "dataType": ["text"]
                    },
                    {
                        "name": "description",
                        "dataType": ["text"]
                    },
                    {
                        "name": "as",
                        "dataType": ["text"]
                    },
                    {
                        "name": "want",
                        "dataType": ["text"]
                    },
                    {
                        "name": "so",
                        "dataType": ["text"]
                    },
                    {
                        "name": "url",
                        "dataType": ["text"],
                        "tokenization": "field"
                    },
                ],
            }
        }

    def getSchemaObject(self):
        return self.class_obj

    def read_json(self):
        try:
            with open(self.file_path, 'r') as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {self.file_path}")
            return None

    def startupSchemaCreate(self, waClient):
        waClient.schema.create_class(self.class_obj)
        return True

    def startupSchemaFeed(self, json_data, client):
        client.batch.configure(batch_size=100)  # Configure batch
        with client.batch as batch:  # Initialize a batch process
            for i, d in enumerate(json_data):  # Batch import data
                print(f"importing question: {i + 1}")
                properties = {
                    "idStartup": d["idStartup"],
                    "category": d["category"],
                    "name": d["name"],
                    "description": d["description"],
                    "as": d["as"],
                    "want": d["want"],
                    "so": d["so"],
                    "url": d["url"],
                }
                batch.add_data_object(
                    data_object=properties,
                    class_name="StartupUserCase"
                )
