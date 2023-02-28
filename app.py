import pickle
from flask import Flask, request, app, jsonify, render_template, url_for
import numpy as np
import pandas as pd

# Initialize the flask App
app = Flask(__name__)

# Load the pickled model and encoder
model = pickle.load(open('car_price_prediction_rf_model.pkl', 'rb'))
encoder = pickle.load(open('car_price_prediction_encoder.pkl', 'rb'))
categorical_columns = ['manufacturer',
                       'model',
                       'condition',
                       'fuel',
                       'transmission',
                       'drive',
                       'type',
                       'paint_color']

# Default page of our web-app


@app.route('/')
def home():
    return render_template('index.html')

# To use the predict button in our web-app


@app.route('/predict', methods=['POST'])
def predict():
    print(request.form)
    # Convert the post request to a dataframe
    instance = pd.DataFrame(request.form, index=[0])
    # Get the order of the columns used for training the model (the same will need to be used for the test example)
    columns = model.feature_names_in_
    # Transform the test example to the same order of columns as the training set
    instance = instance[columns]
    # Convert the age colum value to the actual age of the car
    instance['age'] = 2023 - int(instance['age'])
    instance["odometer"] = int(instance["odometer"])
    # Encode the categorical features
    print(instance)
    instance[categorical_columns] = encoder.transform(
        instance[categorical_columns])

    # Use the model to predict the price
    output = model.predict(instance)[0]
    return render_template('index.html', prediction_text='The estimated of the car is ${}'.format(output))


if __name__ == '__main__':
    app.run(debug=True)
