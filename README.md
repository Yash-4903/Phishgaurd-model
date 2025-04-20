# 🛡️ PhishGuard – Machine Learning Model for Phishing Website Detection

This repository contains the backend machine learning model for **PhishGuard**, a browser extension that detects and flags phishing websites using intelligent URL and content-based feature analysis.

## 💡 Project Overview

PhishGuard leverages a machine learning classifier trained on a labeled dataset of phishing and legitimate websites. The model analyzes various features extracted from URLs and HTML content to identify malicious websites in real time.

## 🔍 Features

- ✅ Binary classification: Phishing or Legitimate
- 🧠 Trained using Random Forest (can be swapped with other models)
- 🔗 Feature engineering from URL patterns, domain properties, and metadata
- 🌐 Designed to be integrated with a browser extension frontend via API

## 🗂️ Repository Structure

```bash
Phishgaurd-model/
├── phishguard_model.pkl        # Trained ML model (pickle format)
├── phishing_model.ipynb        # Jupyter Notebook with training and evaluation
├── phishing_dataset.csv        # Dataset used for training
├── test_urls.csv               # Test URLs for predictions
├── utils.py                    # Feature extraction and preprocessing utilities
├── app.py                      # Flask API for model serving
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
