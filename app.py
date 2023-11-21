from flask import Flask, render_template, request
from flask_cors import CORS
from forms import UrlForm
from scrape_urls import scraper
from typo_correction import get_fuzzy_results

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
CORS(app)


@app.route("/")
def hello_world():
    return "<p>This is the server</p>"


@app.route("/app", methods=['GET', 'POST'])
def url_form():
    form = UrlForm()
    result = []
    corrected_url = ""
    if (form.is_submitted()):
        url = request.form["url"]
        gl = request.form["location"]
        result = get_fuzzy_results(data=scraper(q=url, gl=gl), url=url)
        corrected_url = result[0]["url"]
    return render_template('index.html', form=form, result=result, corrected_url=corrected_url)


if __name__ == "__main__":
    app.run(debug=True)
