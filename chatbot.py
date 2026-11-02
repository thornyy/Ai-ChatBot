
import gradio as gr
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chatbot(message, history):
    if not message.strip():
        return "Please enter a message!"

    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful and friendly AI chatbot."
            }
        ]

        for user, assistant in history:
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": assistant})

        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return "Error: " + str(e)

demo = gr.ChatInterface(
    fn=chatbot,
    title="🤖 AI Chatbot",
    description="Chat with your intelligent AI assistant!"
)

demo.launch()
