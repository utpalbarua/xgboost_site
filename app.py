from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load models
model1 = joblib.load('C:/Users/lenovo/OneDrive/Desktop/xgboost/model1.pkl')
model2 = joblib.load('C:/Users/lenovo/OneDrive/Desktop/xgboost/model2.pkl')

def classify_risk(prediction1, prediction2):
    if prediction1 <= 100:
        risk_level = "🟢 Low Risk: The climate impact is minimal, and environmental conditions are stable."
    elif prediction1 <= 150:
        risk_level = "🟡 Moderate Risk: Some climate changes are noticeable, but they have limited effects."
    elif prediction1 <= 200:
        risk_level = "🟠 High Risk: Significant environmental shifts are happening."
    else:
        risk_level = "🔴 Severe Risk: Major instability, increasing severe weather events."

    if prediction2 <= 25:
        severity = "🟢 Mild: Calm weather, no significant risks."
    elif prediction2 <= 50:
        severity = "🟡 Moderate: Occasional storms, but manageable conditions."
    elif prediction2 <= 75:
        severity = "🟠 Severe: Frequent storms, strong winds, possible disruptions."
    else:
        severity = "🔴 Very Severe: High risk of flooding, damaging storms."
    
    return risk_level, severity

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Convert input values to float explicitly
    features = np.array([[float(data['temperature']), float(data['co2_emissions']), float(data['sea_level_rise']),
                          float(data['precipitation']), float(data['humidity']), float(data['wind_speed'])]])

    prediction1 = float(model1.predict(features)[0])  # Convert to Python float
    prediction2 = float(model2.predict(features)[0])  # Convert to Python float

    response = {
        "climate_risk_index": prediction1,
        "risk_level": "Low Risk" if prediction1 <= 100 else "High Risk",
        "weather_severity_index": prediction2,
        "severity": "Mild" if prediction2 <= 25 else "Severe"
    }

    return jsonify(response)


@app.route('/dataset')
def dataset():
    df = pd.read_csv("C:/Users/lenovo/OneDrive/Desktop/xgboost/climate_change_data.csv")
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
