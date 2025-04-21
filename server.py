from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

openai.api_key = "sk-94ed57931c2c40dfa4f570b0db31488f"

def deepseek_analyze(post):
    try:
        # Call OpenAI API to analyze the post
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that analyzes social media posts for sentiment and trend score. Respond only in JSON format like: {\"sentiment\": \"Positive\", \"trend_score\": 0.87}"
                },
                {
                    "role": "user",
                    "content": f"Analyze the sentiment and trend score of this post: '{post}'"
                }
            ]
        )
        
        # Extract the content from the response
        content = response["choices"][0]["message"]["content"]

        # Parse the JSON response
        parsed = json.loads(content)
        sentiment = parsed.get("sentiment", "Unknown")
        trend_score = float(parsed.get("trend_score", 0))

        return {
            "sentiment": sentiment,
            "trend_score": trend_score
        }
    except json.JSONDecodeError:
        # Handle JSON parsing errors
        return {"error": "Failed to parse response from OpenAI API"}
    except Exception as e:
        # Handle other exceptions
        return {"error": str(e)}


Dummy sentiment and trend analyzer
def dummy_analyze(post):
    sentiments = ["Positive", "Negative", "Neutral"]
    return {
        "sentiment": random.choice(sentiments),
        "trend_score": round(random.uniform(0, 1), 2)
    }

@app.route('/analyze', methods=['POST'])
def analyze_posts():
    data = request.get_json()
    posts = data.get("posts", [])
    results = []

    for post in posts:
        analysis = dummy_analyze(post)
        results.append({
            "text": post,
            "sentiment": analysis["sentiment"],
            "trend_score": analysis["trend_score"]
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
