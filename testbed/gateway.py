from flask import Flask

app = Flask(__name__)


@app.route('/')
def liveness_probe():
    return "server is alive."


@app.route('/func/<string:func_id>')
def call_func(func_id):
    # parse func_id and actually call the function via Docker engine
    # 来一个请求就生成一个不同的容器，做完之后删
    # 放到tdengine吧 (timestamp, func_id, container_id)
    return "function {} is called".format(func_id)


if __name__ == '__main__':
    app.run(port=9211)
