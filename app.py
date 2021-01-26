from flask import Flask
from dao.flask_config import app
from dao.flask_api_config import api

if __name__ == '__main__':
    app.run(debug=True)
