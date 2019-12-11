"""
Mnist Digit Prediction Flask Application - David Gallagher
Emerging Technologies 2019 - Ian McLoughlin
"""
# Imports 
import tensorflow as tf
import base64
import io
import numpy as np
import keras
import json
import imageio

from flask import Flask, escape, request, render_template, url_for, jsonify, make_response
from PIL import Image

# Set Flask Instance
app = Flask(__name__)

# Set Global Variables used in POST method
global model, graph, sess
"""
Resolved Issue: When sending predicted results back to the Client, the following error interrupted the response.
Error while reading resource variable dense_4/kernel from Container: localhost. 
This could mean that the variable was uninitialized. 
Not found: Resource localhost/dense_4/kernel/class tensorflow::Var does not exist.
Proposed Solution: https://github.com/tensorflow/tensorflow/issues/28287 
Resolved - Session needs to be set before calling the model predict.
"""
sess = tf.InteractiveSession()

"""
Running into issues after reshaping my image consistent with my NN model - Prediction must be made using a graph.
ValueError: Tensor Tensor("dense_5/Softmax:0", shape=(?, 10), dtype=float32) is not an element of this graph.
https://datascience.stackexchange.com/questions/48984/valueerror-tensor-tensoractivation-5-softmax0-shape-2-dtype-float32
"""
graph = tf.get_default_graph()

# Load the Saved Model.
def loadKerasModel():
    model = tf.keras.models.load_model('numberPredictor.h5')
    return model

# instance of Trained NN Model
model = loadKerasModel()

# Home Page
@app.route('/')
def homePage():
    return render_template('home.html')

# About the project (may not be complete `_`)
@app.route('/about')
def aboutPage():
    return render_template('about.html')

# https://pythonise.com/series/learning-flask/flask-and-fetch-api
# Retrieve post
# Process the image received from the user so that it matches the image processing in the NN Model.
@app.route('/postmethod', methods = ['POST'])
def post_javascript_data():
    global model, graph

    # Get the request with the image data (Force - Always try and parse data as JSON)
    canvasData = request.get_json(force=True)

    # Get the image data from the request
    encodedCanvasData = canvasData['data']

    # Decode the data from base64 image using base64
    decodedCanvasData = base64.b64decode(encodedCanvasData)

    # Save image as png using IO
    with open('image.png', 'wb') as im:
        im.write(decodedCanvasData)

    # Read saved image in as grayscale using ImageIO
    # Images in MNIST are greyscale so we convert the user image to match what the Model expects
    im = imageio.imread('image.png', pilmode='L')
    
    # Resize the image with Numpy and PIL to the size the Model expects
    imResized = np.array(Image.fromarray(im).resize((28,28)))
    
    # Reshape the image to match Model expectations
    imReshaped = np.array(imResized, dtype=np.float32).reshape(1,784)
    imReshaped /=255

    # Set the Session, Set the Graph, call the model to predict the processed image.
    with sess.as_default():
        with graph.as_default():        
            prediction = model.predict(imReshaped)

    # Printing out the predictions for testing and confirmation of accuracy.
    print("prediction")
    print(np.argmax(prediction))

    # Dumping out the array as JSON so we can sent it to the client in our response.
    # Printing to confirm accuracy
    json_dump = json.dumps({ 'returnData' : prediction }, cls=NumpyEncoder)
    print(json_dump)    

    # Return the response to our client
    # Include our predicted result and our array of prediction percentages
    response = { 'returnPredictionResult' : str(np.argmax(prediction)),
                 'returnAllPredictions' : json_dump}
    return response
    
#  Snippet - json encode the response data (is used in console for now)
#  https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


# App Run
# Start application 
# Host: localhost
# Port: 5050 
# Debug true: Allows reloading of app during development.(Disable before launching anything for production).
 # , debug=True - disabled while testing on Herkou.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)