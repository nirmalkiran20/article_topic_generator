from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate-topics", methods=["POST"])
def generate_topics():
    data = request.get_json()
    keywords = data.get("keywords", [])

    if not keywords:
        return jsonify({"error": "No keywords provided."}), 400

    prompt = (
        "Generate 10 trending blog article ideas based on the following keywords. "
        "Include a topic title, a meta title (max 60 characters), and a meta description (max 155 characters). "
        f"Keywords: {', '.join(keywords)}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates SEO-optimized blog content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        content = response.choices[0].message.content

        # Parse content into list of dicts
        lines = content.strip().split("\n")
        suggestions = []
        temp = {}
        for line in lines:
            if line.startswith("Topic Title:"):
                temp["topic"] = line.replace("Topic Title:", "").strip()
            elif line.startswith("Meta Title:"):
                temp["metaTitle"] = line.replace("Meta Title:", "").strip()
            elif line.startswith("Meta Description:"):
                temp["metaDescription"] = line.replace("Meta Description:", "").strip()
            elif temp:
                temp["keywords"] = ", ".join(keywords)
                suggestions.append(temp)
                temp = {}

        return jsonify(suggestions[:10])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
