from flask import Flask, request, send_file
from TTS.utils.synthesizer import Synthesizer
from io import BytesIO
from pydub import AudioSegment

app = Flask(__name__)

DEFAULT_TTS_MODEL = "tts_models/en/ljspeech/tacotron2-DDC"
DEFAULT_VOCODER = "vocoder_models/en/ljspeech/hifigan_v2"

@app.route('/tts', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data.get('text')
    model = data.get('model', DEFAULT_TTS_MODEL)
    vocoder = data.get('vocoder')
    speaker = data.get('speaker')

    if not text:
        return {"error": "No text provided"}, 400

    # Use default vocoder only if model is the default model and vocoder is not provided
    if model == DEFAULT_TTS_MODEL and not vocoder:
        vocoder = DEFAULT_VOCODER

    # Initialize synthesizer
    synthesizer = Synthesizer(tts_model_name=model, vocoder_model_name=vocoder)

    # Synthesize the text with the specified speaker if provided
    wav = synthesizer.tts(text, speaker_name=speaker)

    # Convert to MP3
    output_mp3 = BytesIO()
    audio_segment = AudioSegment.from_wav(BytesIO(wav))
    audio_segment.export(output_mp3, format="mp3")
    output_mp3.seek(0)

    return send_file(output_mp3, mimetype='audio/mp3', as_attachment=True, attachment_filename='output.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
