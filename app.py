from flask import Flask
from views import views

# instantiate the app
app = Flask(__name__)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

app.register_blueprint(views, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)


