from flask import Flask, render_template, request, redirect, url_for
from util import add_text_to_file, get_text_from_file, _construct_form
from constants import (BLACKLIST_FILE, WHITELIST_FILE, BANNED_WORDS_FILE, SECRET_KEY, WTF_CSRF_SECRET_KEY,
                       MITMDUMP_PATH,
                       FILE_PID, FILE_WEBSITE_VISITED,
                       MITMPROXY_MONITOR_PATH)

import subprocess
import os
import signal
import json

app = Flask(__name__)

app.config.update(dict(
        SECRET_KEY=SECRET_KEY,
        WTF_CSRF_SECRET_KEY=WTF_CSRF_SECRET_KEY
))


@app.route('/')
def index():
    banned_words = get_text_from_file(BANNED_WORDS_FILE)
    white_list = get_text_from_file(WHITELIST_FILE)
    black_list = get_text_from_file(BLACKLIST_FILE)

    websites_visited = {}
    with open('files/websites_visited.json', 'r') as f:
        websites_visited = json.load(f)

    form = _construct_form(banned_words, white_list, black_list)

    return render_template('index.html', form=form, websites_visited=websites_visited)


@app.route('/visualize')
def visualize():
    data = {}
    with open('files/words.json', 'r') as f:
        data = json.load(f)
        data = [{"text": key, "size": val}
                for key, val in data.items()]

    return render_template('visualize.html', data=data)


@app.route('/submit', methods=['POST'])
def submit():
    add_text_to_file(request.form['bannedWords'], BANNED_WORDS_FILE)
    add_text_to_file(request.form['whiteList'], WHITELIST_FILE, url_check=True)
    add_text_to_file(request.form['blackList'], BLACKLIST_FILE, url_check=True)

    return redirect(url_for('index', update="yes"))


@app.route('/start', methods=['POST'])
def start():
    process = subprocess.Popen('%s -s %s' % (MITMDUMP_PATH, MITMPROXY_MONITOR_PATH),
                               shell=True)

    with open(FILE_PID, 'w') as f:
        f.write(str(process.pid))

    return redirect(url_for('index', start="yes"))


@app.route('/stop', methods=['POST'])
def stop():
    with open(FILE_PID, 'r') as f:
        lines = list(f.readlines())
        if lines:
            pid = int(lines[0])
            os.kill(pid, signal.SIGTERM)

    with open(FILE_PID, 'w') as f:
        f.close()

    with open(FILE_WEBSITE_VISITED, 'w') as f:
        f.write("{}")

    with open('files/words.json', 'w') as f:
        f.write("{}")

    return redirect(url_for('index', stop="yes"))
