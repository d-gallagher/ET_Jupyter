from flask import Flask, escape, request, render_template, url_for, jsonify, make_response
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)



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
    # Using Force - Always try and parse data as JSON
    canvasData = request.get_json(force=True)
    print(canvasData)
    dataToReturn = canvasData['data']
    response = { 'returnData' : dataToReturn }
    print(response) 
    return response

# Create and save csv of image data
def create_csv(text):
    unique_id = str(uuid.uuid4())
    with open('images/'+unique_id+'.csv', 'a') as file:
        file.write(text[1:-1]+"\n")
    return unique_id

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)