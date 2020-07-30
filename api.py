from flask import Flask

PORT = 5000

app = Flask(__name__)

def response(text: str):
    return text, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/internal')
def internal():
    return response("internal")

@app.route('/external')
def external():
    return response("external")

@app.route('/cached')
def cached():
    return response("cached")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)