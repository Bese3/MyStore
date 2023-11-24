from flask import Blueprint
app_collection = Blueprint('api', __name__, url_prefix="/api/v1")
from api.v1.collections.user import *