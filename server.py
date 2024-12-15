import binascii
import json
import traceback
import sys
import os


sys.path.append('.')

from flask import Flask, request, Response, send_file
from flask_cors import cross_origin
from pkg.messages import Messages
from pkg.engine import Engine
from pkg.utilities import mel_to_wav

app = Flask(__name__)
engine = Engine()

#Configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
MAX_TEXT_SIZE = 300

# ========== UPDATE WapidAPI KEY ===========
os.environ['RapidAPI_KEY'] = ''


def encodeFileToBase64(file_name):
    file = open(file_name, 'rb')
    data = file.read()
    return binascii.b2a_base64(data, newline=False).decode('utf-8')


def form_error(message, status):
    result = {}
    result['message'] = message
    return Response(json.dumps(result), status=status,
                          mimetype='application/json')


def form_success(audio):
    result = {}
    result['audio'] = audio
    return Response(json.dumps(result), status=200,
                          mimetype='application/json')

@app.errorhandler(429)
@cross_origin()
def ratelimit_handler(e):
    return form_error(Messages.ERR_RLE_A % e.description, 429)

@app.route("/play", methods=['POST'])
@cross_origin()
def play():
    text = request.form.get('text')
    if text is None:
        return form_error(Messages.ERR_TPM, 400)
    if len(text) == 0:
        return form_error(Messages.ERR_TIE, 400)
    if len(text) > MAX_TEXT_SIZE:
        return form_error(Messages.ERR_TTL, 400)
    try:
        waveform, sr = engine.play(text)
        data = mel_to_wav(waveform, sr)
        return send_file(data, mimetype='audio/wav', as_attachment=False)
    except Exception as err:
        print("ERROR: failed to play the text: '{}', {}".format(text, err))
    traceback.print_exception(*sys.exc_info())
    return form_error(Messages.ERR_INT, 500)

if __name__ == '__main__':
    app.run(debug=True, port=SERVER_PORT)
