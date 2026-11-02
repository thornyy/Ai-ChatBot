
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import gradio as gr
import threading

load_dotenv()

app = Flask(__name__)

# Groq API Client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing! Please check your .env file.")

client = Groq(api_key=api_key)


# AI Chatbot Function
def chatbot(message, history):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful and friendly AI assistant."
            }
        ]

        for user, assistant in history:
            messages.append({
                "role": "user",
                "content": user
            })

            messages.append({
                "role": "assistant",
                "content": assistant
            })

        messages.append({
            "role": "user",
            "content": message
            })

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"


# Flask Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Flask Chat API
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Please enter a message!"}), 400

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and friendly AI assistant."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Gradio Chat Interface
demo = gr.ChatInterface(
    fn=chatbot,
    title="🤖 AI Chatbot",
    description="Ask me anything!",
    chatbot=gr.Chatbot(height=400)
)


if __name__ == "__main__":

    # Start Gradio Server
    threading.Thread(
        target=lambda: demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False
        ),
        daemon=True
    ).start()

    # Start Flask Server
    app.run(debug=False)
