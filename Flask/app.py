import tensorflow as tf
import base64
import io
import numpy as np

from flask import Flask, escape, request, render_template, url_for, jsonify, make_response
from flask_cors import CORS
from PIL import Image, ImageFilter
from matplotlib import pyplot as plt
from scipy.misc import imread
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array

app = Flask(__name__)
CORS(app)

def loadKerasModel():
    model = tf.keras.models.load_model('numberPredictor.h5')
    return model

# Load the Trained Model
kModel = loadKerasModel()

# Main project page
@app.route('/')
def homePage():
    return render_template('home.html')

# About the project
@app.route('/about')
def aboutPage():
    return render_template('about.html')

# About the project
@app.route('/testPage',methods = ['GET'])
def testPage():
    return render_template('testPage.html')

# https://pythonise.com/series/learning-flask/flask-and-fetch-api
# Retrieve post
@app.route('/postmethod', methods = ['POST'])
def post_javascript_data():
    # print(request.form.to_dict())
    # Get the request with the image data (Force - Always try and parse data as JSON)
    canvasData = request.get_json(force=True)
    # Get the image data from the request
    encodedCanvasData = canvasData['data']
    # # Decode the data from base64 image
    decodedCanvasData = base64.b64decode(encodedCanvasData)
    # save image as png
    # https://stackoverflow.com/questions/2323128/convert-string-in-base64-to-image-and-save-on-filesystem-in-python
    with open('image.png', 'wb') as im:
        im.write(decodedCanvasData)
    # read saved image in as grayscale
    x = imread('output.png', mode='L')
    # ValueError: Error when checking input: expected flatten_input to have 3 dimensions, but got array with shape (250, 300)
    prediction = kModel.predict(x).toList() 

    print("prediction")
    print(prediction)

    dataToReturn = canvasData['data']
    response = { 'returnData' : dataToReturn }
    print("response") 
    print(response) 
    return response


# # Create and save csv of image data
# def create_img(text):
#     unique_id = str(uuid.uuid4())
#     with open('images/'+unique_id+'.csv', 'a') as file:
#         file.write(text[1:-1]+"\n")
#     return unique_id

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)