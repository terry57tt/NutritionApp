from flask import Blueprint

app = Blueprint('controllers', __name__)

from .accueil import *
from .aliment import *
from .api import *
from .auth import *
from .diete import *
from .reglages import *
from .suivi import *

