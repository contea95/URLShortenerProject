from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)


@app.route('/get', methods=['GET'])
def get():
    return {"hello": "world!"}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
