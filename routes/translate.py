from flask import render_template

def translation_routes(app):

    @app.route('/translate')
    def translate():
        return render_template('translate.html')
