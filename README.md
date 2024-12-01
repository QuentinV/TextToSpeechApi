### Server running on port 8680

## Example of calls

### TTS returns mp3 content

`POST http://localhost:8680/tts`
```json
{
    "text": "Salut comment ça va ? Je m'appelle Sam et c'est un plaisir de te rencontrer.",
    "model": "tts_models/multilingual/multi-dataset/xtts_v2",
    "language": "fr",
    "speaker": "Asya Anara"
}
```

### List available models

`GET http://localhost:8680/models`

### Get speakers for a model

`http://localhost:8680/speakers?model=tts_models/multilingual/multi-dataset/xtts_v2`

Query parameter "model".