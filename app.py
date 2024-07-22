from flask import Flask
from views import views, communities

# instantiate the app
app = Flask(__name__)

# ToDo include communities e.g. (probably via subdomains)
# community = "1337"
# app.register_blueprint(views, url_prefix="/" + community)
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
