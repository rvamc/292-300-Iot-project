from flask import Flask, request, jsonify
from joblib import load
import numpy as np
from flask_cors import CORS
from twilio.rest import Client

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
model = load('my_model.joblib')  # Load your model

# Twilio setup
account_sid = 'AC46c52c3e81a5a1c9b45a765ed55b6270'
auth_token = '9d1e312e4f862df031581cd212d603af'
twilio_client = Client(account_sid, auth_token)
twilio_number = '+13203058269'  # e.g., "+1234567890"
# notify_number = '+917299727169'  # e.g., "+1987654321"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_features = [data['heart_rate'], data['spo2'], data['temperature']]
    input_features = np.array(input_features).reshape(1, -1)
    prediction = model.predict(input_features)
    predicted_class = int(prediction[0])
    
    '''if predicted_class != 0:  # Assuming '0' is normal, and any other class is abnormal
        send_alert_sms(predicted_class)'''
    
    return jsonify({'prediction': predicted_class})

'''def send_alert_sms(predicted_class):
    """Function to send SMS via Twilio when abnormal prediction is detected."""
    try:
        message = twilio_client.messages.create(
            body=f"Alert: An abnormal prediction was detected (class {predicted_class}). Please review immediately.",
            to=notify_number,
            from_=twilio_number
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")'''

@app.route('/send-sms', methods=['POST'])
def send_sms():
    """Endpoint to manually send SMS messages."""
    data = request.get_json()
    message_text = data.get('message', 'Default message if none provided')
    doctor_phone = data.get('to')  # Get the doctor's phone number from the request
    try:
        message = twilio_client.messages.create(
            body=message_text,
            to=doctor_phone,  # Use the doctor's phone number for the SMS
            from_=twilio_number
        )
        return jsonify({'message': 'SMS sent!', 'sid': message.sid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
