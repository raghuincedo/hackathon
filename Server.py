from flask_api import FlaskAPI
from flask import request, Response, jsonify
import jsonpickle
from PIL import Image
import io
import base64
from Image2Text.Write2file import write_to_file
from flask_cors import CORS

# Initialize the Flask application
app = FlaskAPI(__name__)
CORS(app)

# route http posts to this method
@app.route('/api/RecieveText', methods=['POST'])
def RecieveText():
    r = request

    query = r.data['query']
    # build a response dict to send back to client

    response = {'text': 'query recieved succesfully',
                'image': 'image string'
                }

    print(query)

    # encode response using jsonpickle
    #response_pickled = jsonpickle.encode(response)
    response_to_be_sent = jsonify(response)

    print(response_to_be_sent)

    return response_to_be_sent
    #return Response(response = response_to_be_sent, status=200, mimetype="application/json")

# start flask app
app.run(host="10.11.247.218", port=5000)