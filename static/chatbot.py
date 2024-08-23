from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from sklearn.linear_model import LinearRegression
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'


API_KEY = 'AIzaSyCnHiPnc81WluNjSklL6lLR5FO_NbHRCfM'
#'AIzaSyCCrYnLhDIgToWeG4u_nPpQcB9uNJMze0U'
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

medical_keywords = [
    "Computer Vision", "Sports Analytics", "Real-time Monitoring", "Motion Analysis", "Athlete Performance", "Injury Prevention", "Biomechanics", "Pose Estimation", "Gesture Recognition", "Video Analysis", "Artificial Intelligence (AI)", "Deep Learning", "Tracking Systems", "Human Motion Capture", "Sport-Specific Movements", "Performance Enhancement", "3D Reconstruction", "Wearable Technology", "Sensor Fusion", "Machine Learning in Sports"
]




csv_path = 'datasetFile.csv'  
data = pd.read_csv(csv_path)

X = data[['Parameter 1', 'Parameter 2', 'Parameter 3', 'Parameter 4', 'Parameter 5', 'Parameter 6']]
y = data['Parameter 9']
X = X.to_numpy()

model1 = LinearRegression()
model1.fit(X, y)




@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        inputs = [float(request.form[field]) for field in ['Parameter 1', 'Parameter 2', 'Parameter 3', 'Parameter 4', 'Parameter 5', 'Parameter 6']]
        prediction = model1.predict([inputs])
        print(prediction)
        output = "Argument 1" if prediction[0] >= 0.5 else "Argument 2"
        return render_template('predictor.html', prediction_text=f'{output}')
    return render_template('predictor.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chat.html')


@app.route('/coding')
def coding():
    return render_template('coding.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = str(request.form['messageText'])
    
    if not is_medical_query(user_message):
        bot_response_text = "I'm sorry, I can only answer medical-related questions. Please ask a question related to medical topics."
    else:
        bot_response = chat.send_message(user_message)
        bot_response_text = bot_response.text
    return jsonify({'status': 'OK', 'answer': bot_response_text})

def is_medical_query(query):
    return any(keyword in query.lower() for keyword in medical_keywords)



