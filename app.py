#!/usr/bin/env python3

import os
from flask import Flask

from routes.main_routes import main

app = Flask(__name__)

app.secret_key = "super-secret-key"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB limit

app.register_blueprint(main)

if __name__ == "__main__":
	app.run(debug=True)
