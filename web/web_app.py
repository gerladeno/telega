from flask import Flask, request, render_template
from jinja2 import Template

app = Flask(__name__, template_folder="")
name = 'TCM'

template_context = dict(name=name, chat1='fsdfsfs', msg='121d32d23')


@app.route('/')
def index():
    return render_template('index.html', **template_context)


app.run(debug=True)
