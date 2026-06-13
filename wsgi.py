import sys
import os

path = '/home/zelond123/offer-hunter'
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

from a2wsgi import ASGIMiddleware
from app import app

application = ASGIMiddleware(app)
