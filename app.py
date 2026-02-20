from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

conversation_history = [
    {"role": "system", "content": "You are Aditya AI, a helpful assistant."}
]
import os

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
@app.route("/")
def home():
    return render_template("index.html")

MAX_HISTORY = 10  # number of past exchanges to keep

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    conversation_history.append(
        {"role": "user", "content": user_message}
    )

    # Keep only recent messages
    if len(conversation_history) > MAX_HISTORY:
        conversation_history[:] = conversation_history[-MAX_HISTORY:]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation_history
    )

    reply = response.choices[0].message.content

    conversation_history.append(
        {"role": "assistant", "content": reply}
    )

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)