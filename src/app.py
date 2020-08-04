from flask import Flask, request, make_response, redirect, render_template, jsonify
from dao.flask_config import app
from dao.flask_api_config import api

if __name__ == '__main__':
    app.run(debug=True)
