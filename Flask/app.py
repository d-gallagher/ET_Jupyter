from flask import Flask, escape, request, render_template, url_for, jsonify
import uuid

app = Flask(__name__)
# app.debug="True"

# Main project page
@app.route('/')
def homePage():
    return render_template('home.html')

# About the project
@app.route('/about')
def aboutPage():
    return render_template('about.html')

# Retrieve post
@app.route('/postmethod', methods = ['POST'])
def post_javascript_data():
    jsdata = request.form['canvas_data']
    unique_id = create_csv(jsdata)
    params = { 'uuid' : unique_id }
    return jsonify(params)

# Create and save csv of image data
def create_csv(text):
    unique_id = str(uuid.uuid4())
    with open('images/'+unique_id+'.csv', 'a') as file:
        file.write(text[1:-1]+"\n")
    return unique_id

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)