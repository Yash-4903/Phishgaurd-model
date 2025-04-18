from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained phishing detection model
model = joblib.load("phishing_model.pkl")

# ✅ Feature extraction function that matches the trained model
def extract_features(url):
    return {
        "url_length": len(url),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": sum(1 for c in url if not c.isalnum() and c != '/'),
        "num_subdomains": url.count(".") - 1,
        "https": int(url.startswith("https"))
    }

# ✅ List of features expected by the model in correct order
EXPECTED_FEATURES = [
    "url_length",
    "num_digits",
    "num_special_chars",
    "num_subdomains",
    "https"
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "PhishGuard Model API is running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Extract features
        features = extract_features(url)
        input_row = [features[f] for f in EXPECTED_FEATURES]
        input_df = pd.DataFrame([input_row], columns=EXPECTED_FEATURES)

        # Predict using the loaded model
        prediction = model.predict(input_df)[0]

        return jsonify({
            "is_phishing": bool(prediction == 1),
            "url": url,
            "features": features
        })

    except Exception as e:
        print("❌ Prediction error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
