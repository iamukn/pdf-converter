#!/usr/bin/python3

""" Flask app to serve my pdf converter """
from Py_files.db import visitCount, counts
from flask import Flask, render_template, request
from mimetypes import guess_type
import requests
import math
import random
"""instance of the Flask is created"""
app = Flask(__name__)


if __name__ == '__main__':
    
    """ handles the Weather request from weatherapi"""
    def weather():
        url = 'http://api.weatherapi.com/v1/current.json'
        key = '52eb7cb3d32d4cb89a3194620232505'
        states = ["Lagos"]
        city = states[0]

        params = {
        "key":key,
        "q": city
        }
        try:
            res = requests.get(url, params)
            body = res.json()
            return body
        except Exception:
            return "An error occured"
    state = weather()['location']['region']
    temp = "{}°".format(weather()['current']['temp_c'])



    """ handles the get request from the '/' directory"""
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", deg=temp, location=state)
    @app.route('/', methods=["GET"])
    def home():
        return render_template("index.html", deg=temp, location=state)

    @app.route('/docx', methods=["GET"])
    def docx():
        clients_ip = request.environ.get('HTTP_X_FORWRDED_FOR')
        print(clients_ip)
        return render_template("docx.html", deg=temp, location=state)

    """ handles the post request from the pdf recieved"""

    @app.route('/pdf2word', methods=['POST'])
    def convert():
        if request.method == 'POST':
            pdf_file = request.files['Pdf2Word']
            verify = guess_type(pdf_file.filename)[0]
            if verify == "application/pdf":
                return "Got it"
            else:
                return render_template("pdf2doc.html", deg=temp, pdf='file not a word document', location=state)

    @app.route('/docx', methods=['POST'])
    def docx_convert():
        if request.method == 'POST':
            word_file = request.files['word']
            verify = guess_type(word_file.filename)[0]
            if verify == "application/msword":
                return render_template('doc2pdf.html',download='#', pdf='Got it', deg=temp, location=state)
            elif verify == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return render_template('doc2pdf.html',download='#', pdf="Got it", deg=temp, location=state)
            else:
                return render_template('doc2pdf.html',pdf='Please upload a valid docx', download='#', deg=temp, location=state)

    app.run(debug=True, port=5000, host='0.0.0.0')	