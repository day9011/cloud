from flask import Flask, g
from utils.auth import init_auth
import os

cfg_file = os.path.dirname(os.path.abspath(__file__)) + '/../conf/config.yml'

init_auth(cfg_file)

domain_controller = Flask(__name__)
# api = Api(app)

from .resource import role
