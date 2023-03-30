from flask import Flask, render_template, request

app_version = '1.1.0'

app = Flask(__name__)


@app.route('/')
def root():
    #  return render_template('form.html')
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
