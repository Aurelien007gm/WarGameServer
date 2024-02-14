from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world !"



@app.route('/test')
def test():
    return "Hello, ceci est un autre test."

if __name__ == "__main__":
    app.run()