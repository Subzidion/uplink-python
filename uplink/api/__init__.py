from flask import Blueprint

api = Blueprint('api', __name__)

from . import divisions, ranks, generations, merits, personnel, personnelAccounts
