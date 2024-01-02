from flask import Flask
from views import views

# instantiate the app
app = Flask(__name__)

app.register_blueprint(views, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

'''original flask console start up
import sys
sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])
from flask.cli import ScriptInfo
locals().update(ScriptInfo(create_app=None).load_app().make_shell_context())
print("Python %s on %s\nApp: %s [%s]\nInstance: %s" % (sys.version, sys.platform, app.import_name, app.env, app.instance_path))'''
