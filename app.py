from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Initialize OpenAI with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/generate-topics", methods=["POST"])
def generate_topics():
    try:
        data = request.get_json()
        keywords = data.get("keywords", "")
        if not keywords:
            return jsonify({"error": "No keywords provided"}), 400

        # Construct the prompt
        prompt = f"""Generate 10 unique and trending blog article topics based on the following keywords: {keywords}.
Each topic should be ideal for SEO and marketing. Return the response as a list with:
- Title
- Meta Title (under 60 characters)
- Meta Description (under 155 characters)
- Keywords used"""

        # Generate content from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates SEO-friendly blog ideas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1000
        )

        result = response.choices[0].message.content.strip()
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Allow Render to assign its port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
