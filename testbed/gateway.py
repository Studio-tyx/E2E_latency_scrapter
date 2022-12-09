from flask import Flask

app = Flask(__name__)

@app.route('/')
def liveness_probe():
    return "server is alive."


@app.route('/func/<string:func_id>')
def call_func(func_id):
    # parse func_id and actually call the function via Docker engine
    return "function {} is called".format(func_id)


if __name__ == '__main__':
     app.run(port=9211)