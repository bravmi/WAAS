import whisper
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/", methods=['POST'])
def transcribe():
    # Get variables from request
    requestedModel = request.args.get("model", "tiny")
    language = request.args.get("language")
    task = request.args.get("task", "transcribe")

    # Check if model is available
    if requestedModel not in whisper.available_models():
        return "Model not available", 400
    
    # when language is set, check if it is in the whisper.tokenizer.LANGUAGES list
    if language is not None:
        if language not in whisper.tokenizer.LANGUAGES:
            return "Language not supported", 400

    # Check if task is either translate or transcribe
    if task not in ["translate", "transcribe"]:
        return "Task not supported", 400
        
    model = whisper.load_model(requestedModel)
    result = model.transcribe("audio.mp3", language=language, task=task)
    return result["text"]


@app.route("/detect", methods=['POST'])
def detect():
    # get model query parameter
    requestedModel = request.args.get("model", "tiny")

    # Check if model is available
    if requestedModel not in whisper.available_models():
        return "Model not available", 400

    model = whisper.load_model(requestedModel)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio("audio.mp3")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    return {
        "detectedLanguage": max(probs, key=probs.get)
    }


@app.route("/options", methods=['GET'])
def options():
    return {
        "models": whisper.available_models(),
        "languages": whisper.tokenizer.LANGUAGES,
        "tasks": ["translate", "transcribe"]
    }