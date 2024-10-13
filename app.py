from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os

app = Flask(__name__)

# Set up your OpenAI API key
CORS(app)
openai.api_key = ''


@app.route('/')
def index():
    # Serve the index.html file
    return send_from_directory(os.getcwd(), 'index.html')

# Define the chatbot route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # Get user message from the request body

    if not user_input:
        return jsonify({"error": "Message content missing"}), 400

    try:
        # Make an API call to GPT-3.5-turbo-instruct
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=user_input,
            max_tokens=150,
            temperature=0.7
        )

        # Extract the chatbot's reply from the response
        reply = response.choices[0].text.strip()

        # Return the reply as a JSON response
        return jsonify({"response": reply}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

