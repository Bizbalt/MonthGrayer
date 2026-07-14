from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import logging
from logging.handlers import RotatingFileHandler

# configuring logger
# create a handler that rotates when the file reaches 2MB (2 * 1024 * 1024 bytes) with a maximum of 3 backup files
handler = RotatingFileHandler(
    filename=os.path.join("logs", "monthgrayer.log"),
    maxBytes=2_097_152, # 5 MB in bytes
    backupCount=3
)
# Add formatting
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# root logger
root_logger = logging.getLogger()
root_logger.addHandler(handler) # Attach the handler to the logger
root_logger.addHandler(console_handler) # Attach the console handler to the logger
root_logger.setLevel(logging.INFO) # set the logging to info

# inherit from root logger
logger = logging.getLogger(__name__)
app = Flask(__name__)
logger.info("Application instantiated.")

# initialize Limiter and set key function to IP address
# define the path to the data folder
rate_limit_storage_path = os.path.join(os.path.dirname(__file__), 'data', 'ratelimit')

storage_uri = os.getenv('RATELIMIT_STORAGE_URI', 'memory://')
limiter = Limiter(key_func=get_remote_address, app=app, storage_uri=storage_uri)


# ToDo in case I want to ship it as a docker container alike the Raft knowledgebase website: https://github.com/aquasecurity/trivy (for automatic finding of vulnerabilities) and https://github.com/goodwithtech/dockle (for automatic image creation security)

# import of views must happen after initialisation of the limiter so circular import will be circumvented
from views import views
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
