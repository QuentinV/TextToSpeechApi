### Server running on port 8680

## Intro

Image that create a python api `/tts` that uses `Piper` library.

## TTS endpoints returns wav content

`POST http://localhost:8680/tts`

```json
{
  "text": "Salut comment ça va ? Je m'appelle Sam et c'est un plaisir de te rencontrer.",
  "model": "fr_FR-upmc-medium"
}
```

## Available models

- `fr_FR-upmc-medium`: female voice

## Add new model

Copy to `/app/voices/` folder `.onmx` and parameters `.json` files.
