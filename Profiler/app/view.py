import json
import os
import re

from flask import render_template, request, session, jsonify

import app.IOReadWrite as IO
import app.helper as help
from app.profilerapp import app


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def first_page():
    return render_template('index.html')


@app.route('/topic', methods=['GET', 'POST'])
def topic():
    messages = session['messages']
    readability_score, grade_level, readability_info = help.return_readability_score(messages)
    word_count = readability_score['Words_count']
    sentence_count = readability_score['Sentences_count']
    character_count = readability_score['Character_count']
    average_word_count = readability_score['Average_word_count']
    greater_than_6 = readability_score['Greater_than_6']

    return render_template('indicators/topic.html', word_count=word_count, sentence_count=sentence_count,
                           character_count=character_count,
                           average_word_count=average_word_count, greater_than_6=greater_than_6)


@app.route('/personality', methods=['GET', 'POST'])
def personality():
    messages = session['messages']
    return render_template('indicators/personality.html', messages=messages)


@app.route('/education', methods=['GET', 'POST'])
def education():
    messages = session['messages']
    readability_score, grade_level, readability_info = help.return_readability_score(messages)

    return render_template('indicators/education.html', grade_level=grade_level, readability_info=readability_info)


@app.route('/dialect', methods=['GET', 'POST'])
def dialect():
    messages = session['messages']
    return render_template('indicators/dialect.html', messages=messages)


@app.route('/slang', methods=['GET', 'POST'])
def slang():
    messages = session['messages']
    return render_template('indicators/slang.html', messages=messages)


@app.route('/pronomen', methods=['GET', 'POST'])
def pronomen():
    messages = session['messages']
    return render_template('indicators/pronomen.html', messages=messages)


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    user_choices = request.form.get("user-choices")
    json_choices = json.loads(user_choices)

    text_uploaded = json_choices['text']

    if text_uploaded.__len__() > 0:
        session['messages'] = json_choices['text']

    elif 'file' in request.files:
        file_uploaded = request.files.get('file')

        file_info = os.path.splitext(file_uploaded.filename)

        file_type = file_info[1]

        supported_filetype_check = re.compile('(.txt|.docx|.pdf)')

        if supported_filetype_check.match(file_type):
            text = IO.get_data_from_file(file_uploaded, file_type)

            session['messages'] = text

    else:
        return jsonify('System failure')

    return jsonify('success')
