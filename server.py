from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

import numpy as np
import tensorflow as tf
from PIL import Image
import re
import io
import base64

import tensor as ten
import pytesseract as tes

app = Flask(__name__)
api = Api(app)

CORS(app)

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER      

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/parse_table', methods=['POST'])
def upload_file():
    print(request.files)
    # check if the post request has the file part
    if 'file' not in request.files:
        print('no file in request')
        return jsonify({'result': 'No file uploaded'})
    file = request.files['file']
    if file.filename == '':
        print('no selected file')
        return jsonify({'result': 'No file uploaded'})
    if file and allowed_file(file.filename):
        print("file uploaded")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result = getImage(filename)
        return jsonify({'result':result})
    else: 
        return jsonify({'result': 'Upload correct format'})
    print("end")
    return""

def getImage(filename): 
    guess = 0
    if filename:
        #requests image from url 
        img_size = 28, 28 
        # image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # image_string = re.search(r'base64,(.*)', image_url)
        encoded = base64.b64encode(open("/tmp/" + filename, "rb").read())
        image_bytes = io.BytesIO(base64.b64decode(encoded)) 
        image = Image.open(image_bytes) 
        image = image.resize(img_size, Image.LANCZOS)  
        image = image.convert('1') 
        image_array = np.asarray(image)
        image_array = image_array.flatten() 
        
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph('tmp/tensor_model.meta')
            saver.restore(sess, tf.train.latest_checkpoint('tmp/'))
            predict_number = tf.argmax(ten.y, 1)
            predicted_number = ten.sess.run([predict_number], feed_dict={ten.x: [image_array]})
            guess = predicted_number[0][0]
            guess = int(guess)
            print(guess)

        return guess

if __name__ == '__main__':
     app.run(port=5002)