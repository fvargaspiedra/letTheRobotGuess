import sys
import json
import base64
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/classify', methods=['POST'])
def classify():
    if request.method == 'POST':
        data = json.loads(request.data)
        encoded_data = bytes(data['image'].split(',')[1], 'utf-8')
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        croped_img = img[90:390, 170:470]
        ret, thresh = cv2.threshold(croped_img, 80, 255, cv2.THRESH_BINARY)
        cv2.imwrite('thres.png', thresh)
        # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # print(len(contours))
        cv2.imwrite('image.png', thresh)
        guess, accuracy = test_image('image.png')
        return "{\"guess\": \"" + guess.lower() + "\", \"accuracy\": \"" + accuracy.lower() + "\" }"

def test_image(image_name):
    image_data = tf.gfile.FastGFile(image_name, 'rb').read()
    # holt labels aus file in array

    label_lines = [line.rstrip() for line
                  in tf.gfile.GFile("../tf_files/retrained_labels.txt")]
    # !! labels befinden sich jeweils in eigenen lines -> keine aenderung in retrain.py noetig -> falsche darstellung im windows editor !!

    # graph einlesen, wurde in train.sh -> call retrain.py trainiert
    with tf.gfile.FastGFile("../tf_files/retrained_graph.pb", 'rb') as f:

        # The graph-graph_def is a saved copy of a TensorFlow graph; objektinitialisierung
        graph_def = tf.GraphDef()
        # Parse serialized protocol buffer data into variable
        graph_def.ParseFromString(f.read())
        # import a serialized TensorFlow GraphDef protocol buffer, extract objects in the GraphDef as tf.Tensor
        _ = tf.import_graph_def(graph_def, name='')

    #https://github.com/Hvass-Labs/TensorFlow-Tutorials/blob/master/inception.py ; ab zeile 276

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    # return: Tensor("final_result:0", shape=(?, 4), dtype=float32); stringname definiert in retrain.py, zeile 1064

        predictions = sess.run(softmax_tensor,
                              {'DecodeJpeg/contents:0': image_data})
        # gibt prediction values in array zuerueck:

        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    # sortierung; circle -> 0, plus -> 1, square -> 2, triangle -> 3; array return bsp [3 1 2 0] -> sortiert nach groesster uebereinstimmmung

    # output
        # for node_id in top_k:
        #     human_string = label_lines[node_id]
        #     score = predictions[0][node_id]
        #     print('%s (score = %.5f)' % (human_string, score), file=sys.stdout)

        return str(label_lines[top_k[0]]), str(predictions[0][top_k[0]])

@app.route('/getLabels', methods=['GET'])
def getLabels():
    if request.method == 'GET':
        lines = []
        with open("../tf_files/retrained_labels.txt") as file:
            for line in file:
                line = line.strip()
                lines.append(line)
    print(lines, file=sys.stdout)
    linesLower = [item.lower() for item in lines]
    return json.dumps(linesLower)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)

