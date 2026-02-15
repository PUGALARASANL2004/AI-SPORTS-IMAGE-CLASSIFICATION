"""
This file acts as a bridge for hosting platforms that default to searching for 'app:app'.
It redirects the WSGI application from Django's sports_classifier.wsgi.
"""
from sports_classifier.wsgi import application

# This variable 'app' is what Gunicorn/Render look for by default
app = application
