activate_this = '/home/ubuntu/baseball_chatbot/venv/bin/activate_this.py'
with open(activate_this) as f:
	exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/baseball_chatbot/")

<<<<<<< HEAD
from app import app as application
=======
from app import app as application
>>>>>>> web-integration
