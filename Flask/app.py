import tensorflow as tf
import base64
import io
import numpy as np
import keras

from flask import Flask, escape, request, render_template, url_for, jsonify, make_response
# from tensorflow.python.keras.backend import set_session
# from flask_cors import CORS
from PIL import Image, ImageFilter, ImageOps
from matplotlib import pyplot as plt
from scipy.misc import imread, imresize



app = Flask(__name__)
# CORS(app)

# # https://github.com/tensorflow/cleverhans/issues/1117
# session = keras.backend.get_session()
# init = tf.global_variables_initializer()
# session.run(init)

global model, graph, sess
sess = tf.InteractiveSession()
graph = tf.get_default_graph()

"""
Running into issues after reshapint my image consistent with my NN model - 
ValueError: Tensor Tensor("dense_5/Softmax:0", shape=(?, 10), dtype=float32) is not an element of this graph.
https://datascience.stackexchange.com/questions/48984/valueerror-tensor-tensoractivation-5-softmax0-shape-2-dtype-float32
proposed solution:
"""



def loadKerasModel():
    model = tf.keras.models.load_model('numberPredictor.h5')
    return model

# Load the Trained Model
model = loadKerasModel()


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
    global model, graph
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
    im = imread('image.png', mode='L')
    
    # print("im.shape original")
    # print(im.shape)

    imResized = imresize(im, (28,28))
    # print("imResized.shape resized")
    # print(imResized.shape)
    
    
    # imReshaped = np.reshape(imResized, (1,28,28))
    # imReshaped = tf.keras.utils.normalize(imResized, axis=1)
    imReshaped = np.array(imResized, dtype=np.float32).reshape(1,784)
    imReshaped /=255
    # print("imResized.shape reshaped")
    # print(imReshaped.shape)
    # print("Config", app.config)

    """
    See above issue res proposal using graph.
    Current Issue:
    Error while reading resource variable dense_4/kernel from Container: localhost. 
    This could mean that the variable was uninitialized. 
    Not found: Resource localhost/dense_4/kernel/class tensorflow::Var does not exist.
    Proposed Solution: https://github.com/tensorflow/tensorflow/issues/28287 - Unresolved with this solution
    """

    with sess.as_default():
        with graph.as_default():        
            prediction = model.predict(imReshaped)

    print("prediction")
    print(np.argmax(prediction))
    
    # print(prediction)

    # dataToReturn = canvasData['data']
    # dataToReturn = [prediction]
    response = { 'returnData' : prediction }
    # print("response") 
    # print(response) 
    return response


# # Create and save csv of image data
# def create_img(text):
#     unique_id = str(uuid.uuid4())
#     with open('images/'+unique_id+'.csv', 'a') as file:
#         file.write(text[1:-1]+"\n")
#     return unique_id

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)