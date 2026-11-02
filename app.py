
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Groq API Client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing! Please check your .env file.")

client = Groq(api_key=api_key)


# Flask Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Flask Chat API
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid request!"}), 400

        message = data.get("message", "").strip()
        history = data.get("history", [])

        # Validate message
        if not message:
            return jsonify({"error": "Please enter a message!"}), 400

        if len(message) > 500:
            return jsonify({"error": "Message must be under 500 characters!"}), 400

        # Prepare conversation history
        messages = [
            {
                "role": "system",
                "content": "You are a helpful and friendly AI assistant."
            }
        ]

        # Add previous messages
        for item in history:
            if item.get("role") in ["user", "assistant"]:
                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })

        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })

        # Get AI response
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        return jsonify({"response": answer})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Something went wrong. Please try again."}), 500


# Run Flask Application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)