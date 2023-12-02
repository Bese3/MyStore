#!/usr/bin/python3
from flask import Blueprint
app_collection = Blueprint('api', __name__, url_prefix="/api/v1")
from api.v1.collections.user import *
from api.v1.collections.portfolio import *
from api.v1.collections.hobbies import *
from api.v1.collections.books import *
from api.v1.collections.movies import *
from api.v1.collections.music import *
