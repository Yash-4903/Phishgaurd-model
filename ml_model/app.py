@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        url = data.get("url", "")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Extract features
        features = extract_features(url)

        # MATCH this order exactly to your trained model
        expected_features = ['url_length', 'num_digits', 'num_special_chars', 'num_subdomains', 'https']
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
