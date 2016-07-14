from flask import (Flask)

app = Flask(__name__)

from . import core
from . import qcloud
from . import getdata
from . import create
from . import delete
from . import upgrade