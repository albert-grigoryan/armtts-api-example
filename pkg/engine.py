#!/usr/bin/env python
'''
Author Albert Grigoryan
E-mail: albert_grigoryan@yahoo.com
109/26 Vardanants St.,
Yerevan, 0050, Armenia
Tel:  +374-93-635-380
'''

import os
import requests
import json
import re
import onnx
import numpy as np
import onnxruntime as ort

from pkg.utilities import measure_time

MAX_LENGTH = 180
HALF_LENGTH = int(MAX_LENGTH / 2)
SAMPLE_RATE = 44100
RESULTS_DIR = 'results'

class Engine:
    _model_path = None
    _preprocess_api_address = None
    _RapidAPI_Key = None
    _session = None

    def initialize(self):
        self._model_path = os.environ.get('MODEL', 'models/arm-gor.onnx')
        print(f"Running {self._model_path}...")
        self._preprocess_api_address = os.environ.get('PREPROCESS_API_ADDRESS', 'https://armtts1.p.rapidapi.com/v3/preprocess')
        self._RapidAPI_Key = os.environ.get('RapidAPI_KEY', "")
        model = onnx.load(self._model_path)
        self._session = ort.InferenceSession(model.SerializeToString())

    def getIds(self, text):
        payload={'text': text}
        headers = {
            'X-RapidAPI-Key': self._RapidAPI_Key
        }
        print(self._preprocess_api_address)
        response = requests.request("POST", self._preprocess_api_address, headers=headers, files=payload, verify=False)
        if response.status_code != 200:
            print(f"ERROR response: {response.content}")
        return json.loads(response.text)['ids']


    def tokenize(self, text):
        text = self.preprocess_text(text)
        if not text:
            return []

        tokens = []
        while len(text) > 0:
            token, text = self.get_next_token(text)
            tokens.append(token.strip())

        return tokens

    def clean_punctuation(self, text: str) -> str:
        text = re.sub(r'[;։։]', ':', text)
        text = re.sub(r'[՝`]', ',', text)

        text = re.sub(r'․', '.', text)
        text = re.sub(r'(?<!\d)\.(?!\d)', ':', text) # replace . with : if not between numbers
        pattern = r'^[,: ]+|[,: ]+$'
        trimmed_string = re.sub(pattern, '', text)
        return trimmed_string + ":"

    def preprocess_text(self, text):
        """Preprocesses the input text by handling time-like patterns and replacing specific punctuation."""
        text = text.strip()
        if not text:
            return ''

        time_pattern = re.compile(r'([012]?[0-9]):([012345]?[0-9])')
        text = re.sub(time_pattern, r'\1 անց \2', text)

        text = self.clean_punctuation(text)

        return text


    def get_next_token(self, text):
        """Finds the next token based on the current text."""
        if not ':' in text[:MAX_LENGTH] and len(text) <= MAX_LENGTH:
            return text.strip(), ''

        if ':' in text[:MAX_LENGTH]:
            idx = text[:MAX_LENGTH].find(':')
            return text[:idx+1].strip(), text[idx+1:]

        if ',' in text[:MAX_LENGTH]:
            r_idx = text[HALF_LENGTH:MAX_LENGTH].find(',')
            l_idx = text[:HALF_LENGTH].rfind(',')
            if r_idx > (HALF_LENGTH - l_idx):
                return text[:l_idx+1].strip(), text[l_idx+1:]
            else:
                idx = r_idx + HALF_LENGTH
                return text[:idx+1].strip(), text[idx+1:]

        if ' ' in text[:MAX_LENGTH]:
            r_idx = text[HALF_LENGTH:MAX_LENGTH].find(' ')
            l_idx = text[:HALF_LENGTH].rfind(' ')
            if r_idx > (HALF_LENGTH - l_idx):
                return text[:l_idx+1].strip(), text[l_idx+1:]
            else:
                idx = r_idx + HALF_LENGTH
                return text[:idx+1].strip(), text[idx+1:]

        return text[:HALF_LENGTH], text[HALF_LENGTH:]

    def inferenceChunk(self, chunk):
        ids = self.getIds(chunk)
        input_data = np.array([ids], dtype=np.int64)
        input_lengths = np.array([len(ids)], dtype=np.int64)
        scales = np.array([0.333, 1.0, 0.333], dtype=np.float32)
        input_feed = {
            'input': input_data,
            'input_lengths': input_lengths,
            'scales': scales
        }
        audio = self._session.run(None, input_feed)[0][0][0][0]
        return audio

    def generate(self, text):
        result = np.array([], dtype=np.float32)
        tokens = self.tokenize(text)
        print(tokens)
        for chunk in tokens:
            audio = self.inferenceChunk(chunk)
            result = np.concatenate((result, audio), axis=0)
        return result

    @measure_time
    def play(self, text):
        mels = self.generate(text)
        return (mels, SAMPLE_RATE)

    def __init__(self):
        self.initialize()


if __name__ == '__main__':
    engine = Engine()
    print(engine.tokenize("Հայաստան են ժամանելու միջազգային ինչպես նաև տարբեր երկրների պետական կառույցների տարածքային կառավարման կազմակերպությունների ներկայացուցիչներ լրատվամիջոցներ զբոսաշրջության ոլորտի մասնագետներ գինու միջազգային փորձագետներ Սոնա Հովհաննիսյանը նշել է որ մասնակցության հայտ են ներկայացրել տարբեր երկրներից Պորտուգ"))
