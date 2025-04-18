from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained ML model
model = joblib.load("phishingdetection.pkl")

# Feature extraction function
def extract_features(url):
    return {
        "url_length": len(url),
        "num_digits": sum(char.isdigit() for char in url),
        "num_special_chars": sum(1 for char in url if not char.isalnum() and char != '/'),
        "num_subdomains": url.count(".") - 1,
        "https": int(url.startswith("https")),
    }

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "PhishGuard Model API is running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        url = data.get("url", "")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Extract and order features correctly
        features = extract_features(url)
        expected_features = ['url_length', 'num_digits', 'num_special_chars', 'num_subdomains', 'https']
        input_row = [features[f] for f in expected_features]
        input_df = pd.DataFrame([input_row], columns=expected_features)

        # Predict using the trained model
        prediction = model.predict(input_df)[0]

        return jsonify({
            "is_phishing": bool(prediction),
            "url": url
        })

    except Exception as e:
        print("❌ Prediction error:", str(e))
        return jsonify({
            "error": "Prediction failed",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
