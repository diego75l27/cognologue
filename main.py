from dotenv import load_dotenv
import os
import weaviate
import json
import gradio as gr
from schema import startupSchema

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


# Load chat interface
def pythiaChat(message, history):
    return


def respond(message, chat_history):
    response = (
        client.query
        .get("StartupUserCase", ["url", "name"])
        .with_near_text({"concepts": [f"{message}"]})
        .with_generate(single_prompt="Explain {description} and {want} and {so} as you might to a business owner")
        .with_limit(10)
        .do()
    )

    json_dictionary = response["data"]["Get"]["StartupUserCase"]
    #url_list = list(dict.fromkeys(json_dictionary))
    bot_message = ""
    url_dict = {}
    for item in json_dictionary:
        url_dict.update({item["url"]: {"name": item["name"], "explanation": item['_additional']['generate']['singleResult']}})

    for key in url_dict:
        name = url_dict[key]["name"]
        explain = url_dict[key]["explanation"]
        title = f"<h3><a href={key}>{name}</a></h3>"
        text_block = f"<div>{explain}</div>"

        bot_message = f"{bot_message}<div>{title}{text_block}<div><br/><hr/></div></div>"

    chat_history.append((message, bot_message))
    explain = "no explenation"
    return "", chat_history, explain


with gr.Blocks() as demo:
    with gr.Tab("Cognologue"):
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Type here your use case...")
        #explanation = gr.Textbox(label="Explanation")
        clear = gr.ClearButton([msg, chatbot])

        #msg.submit(respond, [msg, chatbot], [msg, chatbot, explanation])
        msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(share=True, server_name="0.0.0.0")
#demo.launch(share=True)
