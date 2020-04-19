from flask import Blueprint
# Creating an instance of this blueprint, main is the name of this blueprint
bp = Blueprint('main', __name__)

from app.main import routes
