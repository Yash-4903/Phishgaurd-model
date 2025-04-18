from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("phishing_model.pkl")

# Features used during training (same order)
EXPECTED_FEATURES = [
    'having_IP_Address',
    'URL_Length',
    'Shortining_Service',
    'having_At_Symbol',
    'double_slash_redirecting'
    # ➕ Add other feature names from phishing.csv if any
]

@app.route("/")
def home():
    return jsonify({"message": "PhishGuard Model API is running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Validate that all expected features are present
        if not all(f in data for f in EXPECTED_FEATURES):
            return jsonify({
                "error": "Missing one or more required features",
                "required_features": EXPECTED_FEATURES
            }), 400

        # Create DataFrame in correct column order
        input_row = [data[f] for f in EXPECTED_FEATURES]
        input_df = pd.DataFrame([input_row], columns=EXPECTED_FEATURES)

        prediction = model.predict(input_df)[0]

        return jsonify({
            "is_phishing": bool(prediction == 1),
            "prediction": int(prediction)
        })

    except Exception as e:
        print("❌ Prediction error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
