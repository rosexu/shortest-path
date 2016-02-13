from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/example')
def example_page():
    return render_template('example.html', name="some text")


if __name__ == '__main__':
    app.run()
