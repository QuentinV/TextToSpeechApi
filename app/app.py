from flask import Flask, request, send_file, jsonify
import os
from TTS.api import TTS
from io import BytesIO
from pydub import AudioSegment
import torch
import numpy
import soundfile

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"

os.environ["COQUI_TOS_AGREED"] = "1"

@app.route('/tts', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data.get('text')
    model = data.get('model')
    speaker = data.get('speaker', None)
    language = data.get('language', None)

    if not text:
        return {"error": "No text provided"}, 400

    if not model:
        return {"error": "No model provided"}, 400

    tts = TTS(model_name=model).to(device)

    wav_list = tts.tts(text=text, speaker=speaker, language=language)

    wav_array = numpy.array(wav_list)
    wav_io = BytesIO()
    soundfile.write(wav_io, wav_array, samplerate=22050, format='WAV')
    wav_io.seek(0)

    # Convert to MP3
    audio_segment = AudioSegment.from_file(wav_io, format="wav")
    output_mp3 = BytesIO()
    audio_segment.export(output_mp3, format="mp3")
    output_mp3.seek(0)

    return send_file(output_mp3, mimetype='audio/mp3')

@app.route('/speakers', methods=['GET']) 
def list_speakers(): 
    model = request.args.get('model') 
    tts = TTS(model) 
    speakers = tts.speakers 
    return jsonify(speakers)

@app.route('/models', methods=['GET']) 
def list_models():  
    return jsonify(TTS().list_models())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
