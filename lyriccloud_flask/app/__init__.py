import os
import sys

from flask import Flask

# Create Flask app
app = Flask(__name__)

# Add the parent directory of 'lyrics_processing' to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

# Import routes after adding to Python path to ensure they can be found
from app import routes