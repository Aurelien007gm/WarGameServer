from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world !"



@app.route('/test')
def test():
    return "Hello, ceci est un autre test."


@app.function_name(name="HttpTrigger1")
@app.route(route="req")
def main(req):
    user = req.params.get("user")
    return f"Hello, {user}!"

if __name__ == "__main__":
    app.run()