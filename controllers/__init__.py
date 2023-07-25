from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, Response

app = Blueprint('controllers', __name__)

from .accueil import *
from .aliment import *
from .api import *
from .authentification import *
from .diete import *
from .reglages import *

