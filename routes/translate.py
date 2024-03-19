from flask import Flask, render_template, request, jsonify
import googletrans
from googletrans import Translator
import gtts
from gtts import gTTS
import time
import langid

def translation_routes(app):
    language_codes = googletrans.LANGUAGES
    languages = [{"code": code, "name": name} for code, name in language_codes.items()]

    def translate_text(text, target_lang):
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        return translation.text

    def detect_language(text):
        # Use langid library to detect language
        lang, _ = langid.classify(text)
        return lang

    @app.route("/translate", methods=["GET", "POST"])
    def translate():
        if request.method == "POST":
            input_text = request.form.get("input_text")

            # Detect the language of the input text
            input_language = detect_language(input_text)

            # Set the target language to "Sinhala" if the input language is "English"
            target_language_name = "Sinhala" if input_language == "en" else "English"

            # Set the correct target language code for translation
            target_language_code = "si" if input_language == "en" else "en"

            translated_text = translate_text(input_text, target_language_code)
            timestamp = int(time.time())
            filename = f"static/translated_audio/op_{timestamp}.mp3"
            tts = gTTS(translated_text, lang=target_language_code)
            tts.save(filename)

            return render_template("translate.html", languages=languages, input_text=input_text,
                                translated_text=translated_text, audio_filename=filename,
                                detected_language=input_language, target_language=target_language_name)

        return render_template("translate.html", languages=languages)


    @app.route("/detect_language", methods=["POST"])
    def detect_language_endpoint():
        input_text = request.form.get("input_text")
        
        # Implement your language detection logic here
        # For simplicity, let's assume you're using langid again
        lang, _ = langid.classify(input_text)
        
        # Return the detected language name
        return jsonify(language_codes.get(lang, "Unknown"))
