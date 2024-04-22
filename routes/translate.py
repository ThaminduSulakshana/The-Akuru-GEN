from flask import Flask, render_template, request, jsonify
import googletrans
from googletrans import Translator
import gtts
from gtts import gTTS
import time
import langid
import re
import nltk
nltk.download('punkt')
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

def translation_routes(app):
    # Get language codes and names for translation options
    language_codes = googletrans.LANGUAGES
    languages = [{"code": code, "name": name} for code, name in language_codes.items()]

    # Function to translate text to the target language
    def translate_text(text, target_lang):
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        return translation.text

    # Function to detect the language of the input text
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

            # Translate the input text to the target language
            translated_text = translate_text(input_text, target_language_code)
            
            # Generate audio for translated text
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
        # Endpoint to detect the language of the input text
        input_text = request.form.get("input_text")
        
        # Use langid library to detect language
        lang, _ = langid.classify(input_text)
        
        # Return the detected language name
        return jsonify(language_codes.get(lang, "Unknown"))
    
    @app.route("/summarization", methods=['GET', 'POST'])
    def summarize():
        if request.method == 'POST':
            inputtext = request.form['inputtext_']
            inputtext = str(re.sub(' +', ' ', inputtext))

            sentence_count = len(re.split(r'[.!?]+', inputtext))

            summarizer = TextRankSummarizer()
            parser = PlaintextParser.from_string(inputtext, Tokenizer('english'))

             # Ranking sentences on the basis of TextRank algorithm and choosing top 2 sentences for summary
            summary_sentences = summarizer(parser.document, round(0.2 * sentence_count))

            summary = ""
            for sentence in summary_sentences:
                summary += str(sentence) + " "
                

            return render_template("translate.html", data={'summary': summary})

        # If the request method is GET or other, just render the template without summarization
        return render_template("translate.html")