import pickle
import json
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the trained model
with open('my_model.pickle', 'rb') as model_file:
    model = pickle.load(model_file)

# Load the column names for one-hot encoding
with open('columns.json', 'r') as columns_file:
    columns_data = json.load(columns_file)
    columns = columns_data['data_columns']

    location_mapping = {location: index for index, location in enumerate(columns[3:])}

# Render the main page
@app.route('/')
def home():
    return render_template('index.html')

# Predict house price
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = np.zeros(len(columns))  # Initialize a numpy array with zeros

        input_data[0] = data.get('0', 0)  # Area
        input_data[1] = data.get('1', 0)  # Bathrooms
        input_data[2] = data.get('2', 0)  # Bedrooms

        if '3' in data:  # Location index
            input_data[3 + location_mapping[data['3']]] = 1  # Set the corresponding location index to 1

        prediction = round(model.predict([input_data])[0],2)
        return jsonify({'predicted_price': prediction})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
