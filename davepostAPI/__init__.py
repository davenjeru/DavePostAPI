from flask import Flask

from davepostAPI.api.v1 import api_v1_blueprint
from davepostAPI.api.v1.auth.login import login_manager as login_manager_v1

# initiate app
app = Flask(__name__)

# configurations
Flask.secret_key = 'secretkey'

# register blueprints
app.register_blueprint(api_v1_blueprint)

# register extensions
login_manager_v1.init_app(app)
