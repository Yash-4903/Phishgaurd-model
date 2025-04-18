from flask import Flask, request, jsonify
import pandas as pd
import joblib
import re

app = Flask(__name__)

# Load trained model
model = joblib.load("phishing_model.pkl")

# Feature extraction from raw URL
def extract_features(url):
    return {
        'having_IP_Address': 1 if re.search(r'((\d{1,3}\.){3}\d{1,3})', url) else 0,
        'URL_Length': -1 if len(url) >= 75 else 0 if len(url) >= 54 else 1,
        'Shortining_Service': 1 if re.search(r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co", url) else 0,
        'having_At_Symbol': 1 if "@" in url else 0,
        'double_slash_redirecting': 1 if url.rfind("//") > 6 else 0
    }

# Feature names expected by the model
EXPECTED_FEATURES = [
    'having_IP_Address',
    'URL_Length',
    'Shortining_Service',
    'having_At_Symbol',
    'double_slash_redirecting'
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "PhishGuard API is running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Extract features from URL
        features = extract_features(url)
        input_row = [features[f] for f in EXPECTED_FEATURES]
        input_df = pd.DataFrame([input_row], columns=EXPECTED_FEATURES)

        prediction = model.predict(input_df)[0]

        return jsonify({
            "is_phishing": bool(prediction == 1),
            "features": features,
            "url": url
        })

    except Exception as e:
        print("❌ Prediction error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
