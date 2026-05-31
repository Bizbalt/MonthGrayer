from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# instantiate the app
app = Flask(__name__)

# initialize Limiter and set key function to IP address
# Define the path to the data folder
rate_limit_storage_path = os.path.join(os.path.dirname(__file__), 'data', 'ratelimit')

storage_uri = os.getenv('RATELIMIT_STORAGE_URI', 'memory://')
limiter = Limiter(key_func=get_remote_address, app=app, storage_uri=storage_uri)


# ToDo in case I want to ship it as a docker container alike the Raft knowledgebase website: https://github.com/aquasecurity/trivy (for automatic finding of vulnerabilities) and https://github.com/goodwithtech/dockle (for automatic image creation security)

# import of views must happen after initialisation of the limiter so circular import will be circumvented
from views import views
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
