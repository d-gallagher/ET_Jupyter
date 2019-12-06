import tensorflow as tf
import base64
import io
import numpy as np
import keras
import json
import imageio

from flask import Flask, escape, request, render_template, url_for, jsonify, make_response

from PIL import Image, ImageFilter, ImageOps
from matplotlib import pyplot as plt
# from scipy.misc import imread, imresize


app = Flask(__name__)

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

# https://pythonise.com/series/learning-flask/flask-and-fetch-api
# Retrieve post
@app.route('/postmethod', methods = ['POST'])
def post_javascript_data():
    global model, graph

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
    im = imageio.imread('image.png', pilmode='L')
    
    # ressize the image - consistent with expected image in the NN 
    # imResized = imresize(im, (28,28))
    imResized = np.array(Image.fromarray(im).resize((28,28)))
    
    
    # imReshaped = np.reshape(imResized, (1,28,28))
    # imReshaped = tf.keras.utils.normalize(imResized, axis=1)
    imReshaped = np.array(imResized, dtype=np.float32).reshape(1,784)
    imReshaped /=255

    """
    See above issue res proposal using graph.
    Current Issue:
    Error while reading resource variable dense_4/kernel from Container: localhost. 
    This could mean that the variable was uninitialized. 
    Not found: Resource localhost/dense_4/kernel/class tensorflow::Var does not exist.
    Proposed Solution: https://github.com/tensorflow/tensorflow/issues/28287 
    Resolved - Session needs to be set before calling the model predict.
    """

    with sess.as_default():
        with graph.as_default():        
            prediction = model.predict(imReshaped)

    print("prediction")
    print(np.argmax(prediction))

    

    # Dumping out the array
    json_dump = json.dumps({ 'returnData' : prediction }, cls=NumpyEncoder)
    print(json_dump)    

    # Return the response to our client
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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)