# Emerging Technologies - Digit Recognition with MNIST, Keras and Tensorflow
###### David Gallagher

### Project Specs
Train a Neural Network(NN) using [Keras](https://keras.io/) and [Tensorflow](https://www.tensorflow.org/). 
The NN will use the [MNIST](http://yann.lecun.com/exdb/mnist/) dataset to train and recognise digits 0-9. We then use that trained NN to predict the number passed to it.

Build a client and server application using [Flask](http://flask.palletsprojects.com/en/1.1.x/). The Flask server will receive an image from the client which has been drawn by the user on a canvas and use the NN to predict what digit is in the image.

### Useful Python links for this project.
* [Python](https://www.python.org/).
* [Tensorflow](https://www.tensorflow.org/).
* [Keras](https://keras.io/).
* [Flask](http://flask.palletsprojects.com/en/1.1.x/).
* [Numpy](https://numpy.org/).
* [Imageio](https://imageio.readthedocs.io/en/stable/).
* [Base64](https://docs.python.org/2/library/base64.html).
* [JSON](https://docs.python.org/3/library/json.html).

### Useful Software links for this project.
* [Anaconda](https://www.anaconda.com/distribution/) packages python libraries commonly used for development.
* [Visual Studio Code](https://code.visualstudio.com/) a lightweight and prominent cross-platform IDE for development.
* [Cmder](https://cmder.net/) a better console/terminal for windows.
* [Github](https://git-scm.com/downloads) to clone and use this repository.

### How to use this repository.
**! _IMPORTANT_: You will need Git [installed locally](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). I also reccommend using [Anaconda](https://www.anaconda.com/distribution/), which includes the packages used in this project.**

##### Open terminal/console in your directory.
* Clone this repository:
```
git clone https://github.com/d-gallagher/ET_Jupyter.git
```
* Change to the Project directory:
```
CD ET_Jupyter
```
* Run the Application
```
python Flask/app.py
```
* Open your preferred browser and go to _localhost:5050_
