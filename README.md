# WaaS - Whisper as a Service

Backend flask application for the Speech To Text service.

This service is powered by [OpenAI Whisper](https://github.com/openai/whisper)

## API Documentation

### POST `/`

Receive the detected text from the audio file.

Query parameters:

- OPTIONAL: language: string (default: automatic detection)
- OPTIONAL: model: string (default: `tiny`)
- OPTIONAL: task: string (default: `transcribe`)
  - `transcribe`: Transcribe audio to text
  - `translate`: Transcribe then translate audio to text
- REQUIRED: form field `file`: mp3 audio file to transcribe

### POST `/detect`

Detect the language of the audio file.

Query parameters:

- OPTIONAL: model: string (default: `tiny`)

### POST `/options`

Get the available options for the service.

Return a JSON object with the following keys:

- `languages`: list of available languages
- `models`: list of available models
- `tasks`: list of available tasks