from flask import Flask, request, jsonify
import pandas as pd
import joblib
import re

app = Flask(__name__)

# Load the trained model
model = joblib.load("phishing_model.pkl")

# Feature extraction function
def extract_features(url):
    return {
        "https": int(url.startswith("https")),
        "num_digits": sum(char.isdigit() for char in url),
        "num_special_chars": sum(1 for char in url if not char.isalnum() and char != '/'),
        "num_subdomains": url.count(".") - 1
    }


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        url = data.get("url", "")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        features = extract_features(url)

        expected_features = ["https", "num_digits", "num_special_chars", "num_subdomains"]
        input_row = [features[f] for f in expected_features]

        input_df = pd.DataFrame([input_row], columns=expected_features)

        prediction = model.predict(input_df)[0]

        return jsonify({
            "is_phishing": bool(prediction),
            "url": url
        })

    except Exception as e:
        print("❌ Prediction error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Use port 10000 for Render
